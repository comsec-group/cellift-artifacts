#include "Vmycell.h"
#include "verilated.h"
#include <verilated_fst_c.h>

#include <iostream>
#include <stdlib.h>

#ifndef TESTBENCH_H
#define TESTBENCH_H

#define PRECISE_RANDOM_INPUTS 1

const int kNumTestsNoTaint = 1000;
const int kNumTestsPerComprehensive = 1000;

const int kNumRandomCfgs = 100;
const int kNumTestsPerRandom = 10000;

const int kResetLength = 5;
// Depth of the trace.
const int kTraceLevel = 6;

typedef Vmycell Module;

// This class implements elementary interaction with the design under test.
class Testbench {
 public:
  /**
   * @param record_trace set to false to skip trace recording
   */
  Testbench(bool record_trace = true,
                   const std::string &trace_filename = "sim.fst")
      : module_(new Module), tick_count_(0l), record_trace_(record_trace) {
    // if (record_trace) {
    //   trace_ = new VerilatedFstC;
    //   module_->trace(trace_, kTraceLevel);
    //   trace_->open(trace_filename.c_str());
    // }
  }

  ~Testbench(void) { close_trace(); }

  void close_trace(void) { /* trace_->close(); */ }

  std::unique_ptr<Module> module_;
 private:
  vluint32_t tick_count_;
  bool record_trace_;
  VerilatedFstC *trace_;

  // Masks that contain ones in the corresponding fields.
  uint32_t id_mask_;
  uint32_t content_mask_;
};

/**
 * Creates a random 32-bit integer. The number of bits to integrate is randomized and there can be collisions: it is fast but not as precise in the number of bits. 
 * 
 * @param width 1 <= width <= 32
 * @param num_integrations the number of bits set in the random integer. Can lead to collisions. May be larger than the width.
 */
uint32_t random_input_fast(int width, int num_integrations) {
  uint32_t ret = 0;

  for (int i = 0; i < num_integrations; i++)
    ret |= 1 << (rand() % width);

  return ret;
}

/**
 * Creates a random n-bit input. This is slower but is precise in the number of bits set. 
 * 
 * @param width 1 <= width <= 32
 * @param num_integrations the number of bits set in the random integer. Must be not larger than the width.
 */
uint32_t random_input_precise(int width, int num_integrations) {
  uint32_t ret = 0;

  assert (num_integrations <= width);

  // If it's easier to start with full-one and insert zeros, then do this.
  uint32_t one_or_zero = 1;
  if (num_integrations > width/2) {
    one_or_zero = 0;
    num_integrations = width-num_integrations;
    ret = ~0;
  }
  
  for (int i = 0; i < num_integrations;) {
    int curr_bit_id = rand() % width;
    int curr_bit_val = (ret >> curr_bit_id) & 0x1;

    // If this bit is already set/unset, then try with a (hopefully) different one.
    if (curr_bit_val != one_or_zero) {
      ret ^= 1 << curr_bit_id;
      i++;
    }
  }

  return ret;
}

/**
 * Creates a random n-bit input with a precision/performance trade-off depending on the PRECISE_RANDOM_INPUTS macro. 
 * 
 * @param width 1 <= width <= 32
 * @param num_integrations the number of bits set in the random integer. Must be not larger than the width.
 */
uint32_t random_input(int width, int num_integrations) {
  if (PRECISE_RANDOM_INPUTS)
    return random_input_precise(width, num_integrations);
  else
    return random_input_fast(width, num_integrations);
}

// Returns a random uint32_t.
static inline uint32_t random_uint32() {
    return ((rand() & 0xFFFF) << 16) | (rand() & 0xFFFF);
}

#endif // TESTBENCH_H

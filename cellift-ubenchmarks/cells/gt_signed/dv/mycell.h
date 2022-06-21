#include "testbench.h"

#ifndef CELL_H
#define CELL_H

#include <chrono>

const int kNumIntsIn  = (DATA_WIDTH+31)/32; // Num integers.
int kCellInWidth = DATA_WIDTH;
int kNumExecutions = 1; // Set automatically. Do not modify.
int kNumInstances = NUM_INSTANCES; // Set automatically. Do not modify.

static inline int hamming_weight(uint64_t n) {
  // int ret = 0;
  // while(n)  {
  //     ret++;
  //     n &= n-1;
  // }
  // return ret;
  return __builtin_popcount(n);
}

// @param exec_time_samples is modified in-place (i.e., reordered to get the median)
static int median(std::vector<uint32_t> &exec_time_samples) {
  size_t mid_id = exec_time_samples.size()/2;
  std::nth_element(exec_time_samples.begin(), exec_time_samples.begin()+mid_id, exec_time_samples.end());
  return exec_time_samples[mid_id];
}

/**
 * @param execution_time_micros is a return parameter. It returns the total execution time in microseconds.
 **/
long long int count_tainted_outputs(Testbench *tb, uint32_t& execution_time_micros) {
  srand(0);

  std::vector<uint32_t> exec_time_samples(kNumExecutions);

  using std::chrono::high_resolution_clock;
  using std::chrono::duration_cast;
  using std::chrono::nanoseconds;

  long long int count_taints = 0;

  assert(kNumIntsIn <= 4);
  uint32_t in_mask[kNumIntsIn];
  for (int mask_elem_id = 0; mask_elem_id < kNumIntsIn; mask_elem_id++) {
    int num_bits_set = std::min(DATA_WIDTH-32*mask_elem_id, 32);
    in_mask[mask_elem_id] = 0;
    for (int i = 0; i < num_bits_set; i++)
      in_mask[mask_elem_id] |= (1 << i);
    printf("In mask %d: %x\n", mask_elem_id, in_mask[mask_elem_id]);
  }

  execution_time_micros = 0;
  execution_time_micros = 0;
  for (int exec_id = 0; exec_id < kNumExecutions; exec_id++) {
    for (int instance_id = 0; instance_id < kNumInstances; instance_id++) {
      for (int mask_elem_id = 0; mask_elem_id < kNumIntsIn; mask_elem_id++) {
        tb->module_->a_i[4*instance_id+mask_elem_id]    = random_uint32() & in_mask[mask_elem_id];
        tb->module_->b_i[4*instance_id+mask_elem_id]    = random_uint32() & in_mask[mask_elem_id];
        tb->module_->a_i_t0[4*instance_id+mask_elem_id] = random_uint32() & in_mask[mask_elem_id];
        tb->module_->b_i_t0[4*instance_id+mask_elem_id] = random_uint32() & in_mask[mask_elem_id];
      }
      for (int other_mask_elem_id = kNumIntsIn; other_mask_elem_id < 4; other_mask_elem_id++) {
        tb->module_->a_i[4*instance_id+other_mask_elem_id]    = random_uint32() & in_mask[other_mask_elem_id];
        tb->module_->b_i[4*instance_id+other_mask_elem_id]    = random_uint32() & in_mask[other_mask_elem_id];
        tb->module_->a_i_t0[4*instance_id+other_mask_elem_id] = random_uint32() & in_mask[other_mask_elem_id];
        tb->module_->b_i_t0[4*instance_id+other_mask_elem_id] = random_uint32() & in_mask[other_mask_elem_id];
      }
    }

    auto t1 = high_resolution_clock::now();
    tb->module_->eval();
    auto t2 = high_resolution_clock::now();

    #if (NUM_INSTANCES >= 64)
      for (int instance_id = 0; instance_id < kNumInstances; instance_id++)
        count_taints += 1UL & tb->module_->out_o_t0[instance_id/64] >> (instance_id%64);
    #else
      for (int instance_id = 0; instance_id < kNumInstances; instance_id++)
        count_taints += 1UL & tb->module_->out_o_t0 >> (instance_id%64);
    #endif

    exec_time_samples[exec_id] = duration_cast<nanoseconds>(t2 - t1).count();
    // std::cout << "Exec time: " << exec_time_samples[exec_id] << std::endl;
  }

  execution_time_micros = median(exec_time_samples);

  return count_taints;
}

#endif // CELL_H

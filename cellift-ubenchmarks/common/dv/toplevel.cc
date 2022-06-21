#include "testbench.h"
#include "mycell.h"

#include <fstream>
#include <string>


static void read_data_width_and_num_executions() {
  // std::ifstream data_width_file("../../../data_width.txt");
  // std::string data_width_str;
  // getline(data_width_file, data_width_str);
  // data_width_file.close();
  // std::cout << "Data width:     " << data_width_str << std::endl;
  // kCellInWidth = stoi(data_width_str);

  std::ifstream num_executions_file("../../../num_executions.txt");
  std::string num_executions_str;
  getline(num_executions_file, num_executions_str);
  num_executions_file.close();
  std::cout << "Num executions: " << num_executions_str << std::endl;
  kNumExecutions = stoi(num_executions_str);

  // std::ifstream num_instances_file("../../../num_instances.txt");
  // std::string num_instances_str;
  // getline(num_instances_file, num_instances_str);
  // num_instances_file.close();
  // std::cout << "Num instances:  " << num_instances_str << std::endl;
  // kNumInstances = stoi(num_instances_str);
}

int main(int argc, char **argv, char **env) {

  Verilated::commandArgs(argc, argv);
  Verilated::traceEverOn(false);

  read_data_width_and_num_executions();

  // Instantiate the DUT instance
  Testbench *tb = new Testbench(false, "../../../traces/sim.fst");

  // Count how many outputs were tainted.
  uint32_t execution_time_micros;
  long long int num_tainted_outputs = count_tainted_outputs(tb, execution_time_micros);
  std::cout << "Total tainted outputs: " << std::dec << num_tainted_outputs << std::endl;
  std::cout << "Execution time: " << std::dec << execution_time_micros << " micros" << std::endl;

  std::cout << "Testbench complete!" << std::endl;

  delete tb;
}
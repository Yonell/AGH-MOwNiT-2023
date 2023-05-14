#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#define ARMA_USE_OPENMP 
#include <armadillo>
#include <graphviz/gvc.h>
#include <string>
#include <chrono>


Agdesc_t Agdirected;

namespace solve_resistors {

	class Node {
		int id;
	public:
		Node(int id) {
			this->id = id;
		}
		int get_id() {
			return id;
		}
		bool operator==(Node second) {
			return this->id == second.get_id() ? true : false;
		}
	};

	class Edge {
		Node& first;
		Node& second;
		float resistance;
		float current = 0;
	public:
		Edge(Node& first, Node& second, float resistance) : first(first), second(second) {
			this->resistance = resistance;
		}
		Node& get_first() {
			return first;
		}
		Node& get_second() {
			return second;
		}
		float get_resistance() {
			return resistance;
		}
		float& access_current() {
			return current;
		}
	};

	class SEM {
	private:
		Node& first;
		Node& second;
		float voltage;
		float current;
	public:
		SEM(Node& first, Node& second, float voltage) : first(first), second(second) {
			this->voltage = voltage;
		}
		SEM(SEM& rhs) : first(rhs.first), second(rhs.second) {
			this->voltage = rhs.voltage;
		}
		float get_voltage() {
			return voltage;
		}
		Node& get_first() {
			return first;
		}
		Node& get_second() {
			return second;
		}
	};

	class Graph {
		int nodes_count;
		int edges_count;
		SEM* sem;
		std::vector<Node> nodes;
		std::vector<Edge> edges;
	public:
		Graph(std::string filename) {
			Agdirected.directed = 1;
			Agdirected.flatlock = 1;
			Agdirected.has_attrs = 0;
			Agdirected.has_cmpnd = 0;
			Agdirected.maingraph = 1;
			Agdirected.no_loop = 0;
			Agdirected.no_write = 1;
			Agdirected.strict = 0;
			std::ifstream inFile;
			inFile.open(filename);
			inFile >> this->nodes_count;
			inFile >> this->edges_count;
			for (int i = 0; i < this->nodes_count; i++) {
				nodes.push_back(Node(i));
			}
			for (int i = 0; i < this->edges_count; i++) {
				int first, second;
				float resistance;
				inFile >> first;
				inFile >> second;
				inFile >> resistance;
				edges.push_back(Edge(nodes.at(first), nodes.at(second), resistance));
			}
			int first, second;
			float amount;
			inFile >> first;
			inFile >> second;
			inFile >> amount;
			this->sem = new SEM(nodes.at(first), nodes.at(second), amount);
		}

		std::vector<Node> get_nodes() {
			return nodes;
		}

		std::vector<Edge> get_edges() {
			return edges;
		}

		SEM get_sem() {
			return *sem;
		}

		int find_edge(int first, int second) {
			for (int i = 0; i < edges.size(); i++) {
				if (edges[i].get_first() == first && edges[i].get_second() == second) {
					return i;
				}
			}
			return -1;
		}

		std::vector<int> neighbours(int n) {
			std::vector<int> v;
			for (Edge i : edges) {
				if (i.get_first().get_id() == n) v.push_back(i.get_second().get_id());
				if (i.get_second().get_id() == n) v.push_back(i.get_first().get_id());
			}
			if (sem->get_first().get_id() == n) v.push_back((*sem).get_second().get_id());
			if (sem->get_second().get_id() == n) v.push_back((*sem).get_first().get_id());
			return v;
		}

		int get_nodes_count() {
			return nodes_count;
		}
	};

	void dfs(Graph graph, int node_id, int parent_id, std::vector<std::vector<int>>& cycles, std::vector<int>& colors, std::vector<int>& parents) {
		if (colors[node_id] == 1) {
			std::vector<int> v;

			int cur = parent_id;
			v.push_back(cur);

			while (cur != node_id) {
				cur = parents[cur];
				v.push_back(cur);
			}
			cycles.push_back(v);
			return;
		}

		parents[node_id] = parent_id;
		colors[node_id] = 1;

		for (int v : graph.neighbours(node_id)) {

			if (v == parents[node_id]) {
				continue;
			}
			dfs(graph, v, node_id, cycles, colors, parents);
		}
		colors[node_id] = 0;
	}

	bool is_vec_perm(std::vector<int>& first, std::vector<int>& second) {
		if (first.size() != second.size()) {
			return false;
		}

		int len = first.size();
		for (int i = 0; i < len; ++i) {
			if (first == second) {
				return true;
			}
			second.push_back(second.at(0));
			second.erase(second.begin());
		}

		std::reverse(second.begin(), second.end());

		for (int i = 0; i < len; ++i) {
			if (first == second) {
				return true;
			}
			second.push_back(second.at(0));
			second.erase(second.begin());
		}

		return false;
	}

	void remove_duplicate_cycle(std::vector<std::vector<int>>& vec) {
		for (int i = 0; i < vec.size(); i++) {
			for (int j = i + 1; j < vec.size(); j++) {
				if (is_vec_perm(vec[i], vec[j])) {
					vec.erase(vec.begin() + j);
				}
			}
		}
	}

	std::vector<std::vector<int>> find_distinct_cycles(Graph graph) {
		std::vector<std::vector<int>> cycles;

		std::vector<int> colors(graph.get_nodes_count());
		for (auto& i : colors) {
			i = 0;
		}

		std::vector<int> parents(graph.get_nodes_count());
		for (auto& i : parents) {
			i = 0;
		}

		dfs(graph, 0, -1, cycles, colors, parents);

		remove_duplicate_cycle(cycles);

		return cycles;
	}

	void show_graph(Graph graph, std::vector<float> currents) { // doesnt work
		Agraph_t* G;
		char* first_arg = new char[20];

		first_arg[0] = 'G';
		first_arg[1] = 0;
		G = agopen(first_arg, Agdirected, NULL);

		std::vector<Agnode_t*> nodes;
		std::vector<Agedge_t*> edges;
		for (int i = 0; i < graph.get_nodes_count(); ++i) {
			std::string hehe("n");
			hehe += std::to_string(i);
			char* node_name = (char*)((hehe).c_str());
			nodes.push_back(agnode(G, node_name, TRUE));
		}

		for (int i = 0; i < graph.get_edges().size(); ++i) {
			std::string hehe("e");
			hehe += std::to_string(i);
			char* edge_name = (char*)((hehe).c_str());
			if (currents[i] > 0)
				edges.push_back(agedge(G, nodes[graph.get_edges()[i].get_first().get_id()], nodes[graph.get_edges()[i].get_second().get_id()], edge_name, TRUE));
			else
				edges.push_back(agedge(G, nodes[graph.get_edges()[i].get_second().get_id()], nodes[graph.get_edges()[i].get_first().get_id()], edge_name, TRUE));
		}

		GVC_t* gvc;
		gvc = gvContext();
		gvLayout(gvc, G, "neato"); // nie dziala :c
		gvRender(gvc, G, "plain", stdout);
		gvLayout(gvc, G, "dot");
		gvRender(gvc, G, "plain", stdout);
		gvFreeLayout(gvc, G);

		return;
	}

	std::vector<float> solve(Graph graph) {
		int equation_count = graph.get_nodes_count();
		std::vector<std::vector<int>> cycles = find_distinct_cycles(graph);
		equation_count += cycles.size();

		arma::mat A(equation_count, graph.get_edges().size()+1); // Licze tez natezenie przechodzace przez sem
		arma::vec B(equation_count);

		for (int i = 0; i < graph.get_nodes_count(); ++i) {
			for (auto j : graph.neighbours(i)) {
				int edge_id = graph.find_edge(i, j);
				if (edge_id < 0) {
					edge_id = graph.find_edge(j, i);
					if (edge_id < 0) { // sem
						A(i, graph.get_edges().size()) = ((i == graph.get_sem().get_second().get_id()) ? 1 : -1);
					}
					else { // wchodzaca
						A(i, edge_id) = 1;
					}
				}
				else { // wychodzaca
					A(i, edge_id) = -1;
				}
			}
			B(i) = 0;
		}

		int i = graph.get_nodes_count();

		for(auto j : cycles) {

			for (int k = 0; k < j.size(); ++k) {
				int edge_id = graph.find_edge(j[k], j[(k + 1) % j.size()]);
				if (edge_id < 0) {
					edge_id = graph.find_edge(j[(k + 1) % j.size()], j[k]);
					if (edge_id < 0) { // sem
						B(i) = (j[(k + 1) % j.size()] == graph.get_sem().get_second().get_id()) ? graph.get_sem().get_voltage() : -graph.get_sem().get_voltage();
					}
					else { // wchodzaca
						A(i, edge_id) = -graph.get_edges().at(edge_id).get_resistance();
					}
				}
				else { // wychodzaca
					A(i, edge_id) = graph.get_edges().at(edge_id).get_resistance();
				}
			}
			++i;
		}

		arma::vec result = arma::solve(A, B); // solving Ax = B

		std::vector<float> act_result;
		for (int i = 0; i < graph.get_edges().size()+1; ++i) {
			act_result.push_back(result[i]);
		}
		
		return act_result;
	}

	void export_solution(Graph graph, std::vector<float> currents) {
		std::ofstream out_file;
		out_file.open("./resistor_graph_temp.tmp");
		out_file << graph.get_nodes_count() << "\n";
		out_file << graph.get_edges().size() << "\n";

		for (int i = 0; i < graph.get_edges().size(); ++i) {
			if (currents[i] > 0)
				out_file << graph.get_edges()[i].get_first().get_id() << " " << graph.get_edges()[i].get_second().get_id() << " " << graph.get_edges()[i].get_resistance() << " " << currents[i] << "\n";
			else
				out_file << graph.get_edges()[i].get_second().get_id() << " " << graph.get_edges()[i].get_first().get_id() << " " << graph.get_edges()[i].get_resistance() << " " << -currents[i] << "\n";
		}
		out_file << graph.get_sem().get_first().get_id() << " " << graph.get_sem().get_second().get_id() << " " << graph.get_sem().get_voltage() << " " << currents[graph.get_edges().size()] << "\n";

		out_file.close();

		return;
	}

	bool check_graph(Graph graph, std::vector<float> result) {
		for (int i = 0; i < graph.get_nodes_count(); ++i) {
			float sum = 0;
			for (int j = 0; j < graph.get_edges().size(); ++j) {
				if (i == graph.get_edges()[j].get_first().get_id()) {
					sum -= result[j];
				}
				else if (i == graph.get_edges()[j].get_second().get_id()) {
					sum += result[j];
				}
			}

			if (i == graph.get_sem().get_first().get_id()) {
				sum -= result[graph.get_edges().size()];
			}
			else if (i == graph.get_sem().get_second().get_id()) {
				sum += result[graph.get_edges().size()];
			}

			if (sum > 0.0001) {
				return false;
			}
		}

		return true;
	}
}

int main() {
	std::cout << "Enter file name: ";
	std::string filename;
	std::cin >> filename;
	std::cout << "Loading the graph..." << "\n";
	solve_resistors::Graph graph = solve_resistors::Graph(filename);
	std::cout << "Done!" << "\n";

	std::cout << "Solving the graph..." << "\n";
	auto start = std::chrono::high_resolution_clock().now();
	std::vector<float> result = solve_resistors::solve(graph);
	auto stop = std::chrono::high_resolution_clock().now();
	std::cout << "Done!" << "\n";
	std::cout << "Time elapsed: " << std::chrono::duration_cast<std::chrono::milliseconds>(stop - start).count() << "ms" << "\n";

	std::cout << "Tests: " << (solve_resistors::check_graph(graph, result) ? "PASSED" : "FAILED") << "\n";

	solve_resistors::export_solution(graph, result);

	system("python ./graphVisualizer/graphVisualizer.py"); // u mnie nie dziala :c
	
	return 0;
}
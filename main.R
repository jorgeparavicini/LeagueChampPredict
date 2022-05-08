library("igraph")

graph <- read_graph(
  "D:/Network Analysis/na/na/hue.graphml",
  format="graphml"
)

plot(graph)

# make_largest_diameter_graph <- function(n) {
#   mat <- matrix(0, n, n)
#   for (i in 1:(n - 1)) {
#     mat[i, i + 1] <- 1
#     mat[i + 1, i] <- 1
#   }
#
#   return(graph_from_adjacency_matrix(mat, mode = "undirected"))
# }
#
# make_smallest_diameter_graph <- function(n) {
#   mat <- matrix(1, n, n)
#   for (i in 1:n) {
#     mat[i, i] <- 0
#   }
#
#   return(graph_from_adjacency_matrix(mat, mode = "undirected"))
# }
#
# g <- make_largest_diameter_graph(10)
# plot(g)
# print(centralization.betweenness(g))
# print(centralization.closeness(g))
# print(centralization.degree(g))
#
#
# g <- make_smallest_diameter_graph(10)
# plot(g)
# print(centralization.betweenness(g))
# print(centralization.closeness(g))
# print(centralization.degree(g))

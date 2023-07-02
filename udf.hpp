inline double vector_distance_euclidean_straight(const ListAccum < double > & list1, const ListAccum < double > & list2, int dim) {
    double distance = 0.0;
    for (size_t i = 0; i < dim; ++i) {
        double diff = list1.get(i) - list2.get(i);
        distance += diff * diff;
    }
    return distance;
}
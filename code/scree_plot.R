# Sum of squared error (SSE) scree plot of linguistic data. 
#The location of the elbow in the plot suggests a suitable number of clusters for the k-means.

#specify ID variables
ids <- c(names(lingBinary[,1:6]))

# Create scree plot
wss <- (nrow(lingBinary[,!(names(lingBinary) %in% ids)])-1)*sum(apply(lingBinary[,!(names(lingBinary) %in% ids)],2,var))
for (i in 2:15) wss[i] <- sum(kmeans(lingBinary[,!(names(lingBinary) %in% ids)],
                                     centers=i)$withinss)
plot(1:15, wss, type="b", xlab="Number of clusters",
     ylab="Within groups sum of squares")
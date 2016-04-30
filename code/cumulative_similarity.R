#Plot overlay of the cumulative distributions of the correlation similarity measure for 
# n=100$ runs and increasing values of $k$

results <- read.csv("results.csv",sep =",",
                    col.names=c("k.2", "k.3", "k.4", "k.5", "k.6","k.7","k.8","k.9","k.10"), 
                    fill=TRUE, strip.white=TRUE,header=TRUE)
results.melt <- melt(results)
colnames(results.melt) <- c("k","similarity")
#produce overlayed CDF plot
ggplot(results.melt, aes(similarity, colour = k)) + 
  stat_ecdf() + 
  ylab("Cumulative") +
  xlab("Similarity") +
  scale_color_discrete("k=",
                       labels=c("1","2","3","4","5","6","7","8","9","10"))
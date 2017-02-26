## copy from http://blog.fens.me/r-game-snake/

# 初始化环境变量
init <- function() {
    e <<- new.env()
    e$stage <- 0 # 场景
    e$width <- e$height <- 20
    e$step <- 1 / e$width
    # matrix(data, nrow), 将data（vector）转为矩阵
    # rep(data, times), 将data复制为times倍
    e$m <- matrix(rep(0, e$width * e$height), nrow = e$width)
    e$dir <- e$lasted <- 'up'
    e$head <- c(2, 2)
    e$lastx <- e$lasty <- 2
    e$tail <- data.frame(x=c(), y=c())

    e$col_fruit <- 2
    e$col_head <- 4
    e$col_tail <- 8
    e$col_path <- 0
}

# 获取矩阵的索引值
# 输入是一个值（颜色），返回矩阵里是这个值的索引！
# 配合length() 可以用来判断矩阵中是否有 col 这个颜色(值)
# which(True_Vector), 参数是一个True、False的vector, 如果存在True则返回对应的索引
index <- function(col) which(e$m == col)

# 游戏中

stage1 <- function() {
    e$stage <- 1
    fruit <- function() {
        if (length(index(e$col_fruit)) <= 0) {
            # 无水果
            # 从 “路”中选一个当做水果
            idx <- sample(index(e$col_path), 1)
            # 设置坐标！idx -> (x, y) , idx是顺序号，按行递增的
            # ifelse(test, yes, no) !!
            fx <- ifelse(idx %% e$width == 0, 10, idx %% e$width)
            fy <- ceiling(idx / e$height)
            e$m[fx, fy] <- e$col_fruit
            print(paste("fruit idx", idx))
            print(paste("fruit axis:", fx, fy))
        }
    }

    fail <- function() {
        # head 出边界
        if (length(which(e$head < 1)) > 0 | length(which(e$head > e$width) > 0)) {
            print("game over: Out of ledge.")
            keydown('q')
            return(TRUE)
            }
        # head 碰到 tail( 头位置的颜色是尾巴的颜色，就说明头撞到尾巴了！)
        if (e$m[e$head[1], e$head[2]] == e$col_tail) 
        {
            print("game over: head hit tail")
            keydown('q')
            return(TRUE)
        }
        return(FALSE)

        }
    head <- function(){
        # 先将头部的坐标保存起来
        e$lastx <- e$head[1]
        e$lasty <- e$head[2]

        # 方向
        if(e$dir == 'up') e$head[2] <- e$head[2] + 1
        if(e$dir == 'down') e$head[2] <- e$head[2] - 1
        if(e$dir == 'left') e$head[1] <- e$head[1] - 1
        if(e$dir == 'right') e$head[1] <- e$head[1] + 1
    }
    
    # snake body
    body <- function(){
        e$m[e$lastx, e$lasty] <- 0
        e$m[e$head[1], e$head[2]] <- e$col_head
        # rbind  输入A、B，按行把B添加到A中！
        if(length(index(e$col_fruit)) <= 0){
            e$tail <- rbind(e$tail, data.frame(x=e$lastx, y=e$lasty)) 
        }

        # 下面的逻辑是： 如果有尾巴，那么就先把头(未移动的头，即 lastx, lasty) 加入到尾巴中，同时把尾巴中最后面的一个（最开始加入的那个）从尾巴中移除掉。
        if(nrow(e$tail) > 0){

            e$tail <- rbind(e$tail, data.frame(x=e$lastx, y=e$lasty))
            # tail[1, ]表示取tail 的 第1行（R从1开始计数）， 而 tail[1]表示取第1列！ tail[1, 1]则表示取第一行、第一列
            e$m[e$tail[1,]$x, e$tail[1, ]$y] <- e$col_path
            # 注意！！ tail[-1, ] 表示的是从tail中去掉第1行！！ （而非取倒数第一行！这个真是差别有点大...）
            e$tail <- e$tail[-1,]
            e$m[e$lastx, e$lasty] <- e$col_tail
        }

        print(paste("snake idx", index(e$col_head)))
        print(paste("snake axis: ", e$head[1], e$head[2]))
    }

    drawTable <- function(){
        plot(0, 0, xlim=c(0, 1), ylim=c(0, 1), type='n', xaxs="i", yaxs="i")
    }

    drawMatrix <- function(){
        # which 返回的是 矩阵的一维索引，这个一维索引是按列数的！就是说，先数第一列，输数第二列...
        idx <- which(e$m > 0)
        px <- (ifelse(idx%%e$width==0, e$width, idx%%e$width) - 1)/e$width + e$step / 2
        py <- (ceiling(idx / e$height) - 1) / e$height + e$step / 2
        pxy = data.frame(x=px, y=py, col=e$m[idx])
        # points 是绘图函数！pch 是在坐标处绘制的符号， cex是膨胀率
        points(pxy$x, pxy$y, col=pxy$col, pch=15, cex=4.4)
    }

    fruit()
    head()
    if(!fail()){
        body()
        drawTable()
        drawMatrix()
    }
}

stage0 <- function(){
    e$stage <- 0
    plot(0, 0, xlim=c(0, 1), ylim=c(0, 1), type='n', xaxs="i", yaxs="i")
    text(0.5, 0.7, label="Sanke Game", cex=5)
    text(0.5, 0.4, label="Any keyboard to start", cex=2, col=4)
    text(0.5, 0.3, label="Up, Down, Left, Right to control direction", cex=2, col=2)
    text(0.2, 0.05, label="Author: DanZhang", cex=1)
    text(0.5, 0.05, label="http://blog.fens.me", cex=1)

}

stage2 <- function(){
    e$stage <- 2
    plot(0, 0, xlim=c(00, 1), ylim=c(0, 1), type='n', xaxs="i", yaxs="i")
    text(0.5, 0.7, label="Game Over", cex=5)
    text(0.5, 0.4, label="Space to restart, q to quit.", cex=2, col=4)
    text(0.5, 0.3, label=paste("Congratulations! You have eat", nrow(e$tail), "fruits"))
    text(0.2, 0.05, label="Author: DanZhang", cex=1)
    text(0.5, 0.05, label="http://blog.fens.me", cex=1)


}

keydown <- function(K){
    print(paste("keydown: ", K, "stage: ", e$stage))
    if(e$stage == 0){
        init()
        stage1()
        return(NULL)
    }

    if(e$stage==2){
        if(K=='q'){
            q()
        }
        else if(K == ' '){
            stage0()
        }
        return(NULL)
    }

    if(e$stage==1){

        if(K=="q"){
            stage2()
        }else{
            if(tolower(K) %in% c("up", "down", "left", "right")){
                e$lasted <- e$dir
                e$dir <- tolower(K)
                stage1()
            }
        }
    }
    return(NULL)
}

run <- function(){
    par(mai=rep(0, 4), oma=rep(0, 4))
    e<<- new.env()
    stage0()

    getGraphicsEvent(prompt="Snake Game", onKeybd=keydown)


}

run()
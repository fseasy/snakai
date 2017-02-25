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
        # head 碰到 tail
        if (e$m[e$head[1], e$head[2]] == e$col_tail) 
        {
            print("game over: head hit tail")
            keyword('q')
            return(TRUE)
        }
        return(FALSE)

        }
    head <- function(){
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

        if(nrow(e$trail) > 0){
            e$tail <- rbind(e$tail, data.fram(x=e$lastx, y=e$lasty))
            e$m[e$tail[1,]$x, e$tail[1, ]$y] <- e$col_path
            e$tail <- e$tail[-1,]
            e$m[e$lastx, e$lasty] <- e$col_tail
        }

        print(paste("snake idx", index(e$col_head)))
        print(paste("snake axis: ", e$head[1], e$head[2]))
    }





    }
 }






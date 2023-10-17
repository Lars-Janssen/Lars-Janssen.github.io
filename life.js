let grid;
let next;
let cols;
let rows;
let resolution = 5;

function setup()
{
    background(0);
    cols = int(screen.width / resolution);
    rows = int(screen.height / resolution - 260 / resolution);
    createCanvas(cols * resolution, rows * resolution);
    grid = make2DArray(cols, rows);
    for (let i = 0; i < cols; i++)
    {
        for (let j = 0; j < cols; j++)
        {
            fill(0);
            noStroke(0);
            rect(i * resolution, j * resolution, resolution, resolution);
            grid[i][j] = floor(random(2));
        }
    }
    stroke(0);
}

function draw()
{
    next = make2DArray(cols, rows);

    //Check if mouse is pressed
    if (mouseIsPressed)
    {
        drawing();
    }
    else
    {
        // Compute next based on grid
        for (let i = 0; i < cols; i++)
        {
            for (let j = 0; j < cols; j++)
            {
                let state = grid[i][j];

                // Count live neighbours
                let neighbors = countNeighbors(grid, i, j);

                if (state == 0 && neighbors == 3)
                {
                    fill(255);
                    rect(i * resolution, j * resolution, resolution-1, resolution-1);
                    next[i][j] = 1;
                } 
                else if (state == 1 && (neighbors < 2 || neighbors > 3))
                {
                    fill(0);
                    rect(i * resolution, j * resolution, resolution-1, resolution-1);
                    next[i][j] = 0;
                }
                else
                {
                    next[i][j] = state;
                }
            }
        }
        grid = next;
    }

}

function make2DArray(cols, rows)
{
    let arr = new Array(cols);
    for (let i = 0; i < arr.length; i++)
    {
        arr[i] = new Array(rows);

    }
    return arr;
}

function countNeighbors(grid, x, y)
{
    let sum = 0;
    for (let i = -1; i < 2; i++)
    {
        for (let j = -1; j < 2; j++)
        {
            let col = (x + i + cols) % cols;
            let row = (y+ j + rows) % rows;
            sum += grid[col][row]
        }
    }

    sum -= grid[x][y];
    return sum;
}



function drawing()
{
    if(mouseIsPressed)
    {
        let posX = mouseX;
        let posY = mouseY;
        let row = int(mouseX / resolution);
        let column = int(mouseY / resolution);
        grid[row][column] = 1;
        fill(255);
        rect(row * resolution, column * resolution, resolution-1, resolution-1);
    }
}
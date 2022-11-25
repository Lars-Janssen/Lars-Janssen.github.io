let x;
let y;
let dir = 3;
let resolution = 5;
let fr = 600;

function setup()
{
    cols = int(screen.width / resolution);
    rows = int(screen.height / resolution - 260 / resolution);
    x = int(cols / 2) * resolution;
    y = int(rows / 2) * resolution;

    createCanvas(cols * resolution, rows * resolution);
    background(255);
    frameRate(fr);

    grid = make2DArray(cols, rows);
    for (let i = 0; i < cols; i++)
    {
        for (let j = 0; j < cols; j++)
        {
            grid[i][j] = 0;
        }
    }

}

function draw()
{   
    noStroke();
    for (let i = 0; i < int(fr / 60); i++)
    {
        step(grid);
    }
    fill(255, 0, 0);
    rect(x, y, resolution, resolution);

}

function step(grid)
{
    i = x / resolution;
    j = y / resolution;
    if (grid[i][j] == 0)
    {
        dir = (dir + 1) % 4;
        grid[i][j] = 1;
        fill(0);
        rect(x, y, resolution, resolution);
    }
    else if (grid[i][j] == 1)
    {
        dir = (dir + 3) % 4;
        grid[i][j] = 0;
        fill(255);
        rect(x, y, resolution, resolution);
    }

    if (dir == 0)
    {
        j = (j + rows - 1) % rows;
    }
    else if (dir == 1)
    {
        i = (i + 1) % cols;
    }
    else if (dir == 2)
    {
        j = (j + 1) % rows;
    }
    else if (dir == 3)
    {
        i = (i+ cols - 1) % cols;
    }

    x = i * resolution;
    y = j * resolution;
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

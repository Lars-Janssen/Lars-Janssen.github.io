let grid;
let age;
let cols;
let rows;
let bottom;

let resolution = 15;
let f = 0.00001;
let p = 0.001;
let h = 0.4;
let mature = 50;


function setup()
{
    cols = int(screen.width / resolution);
    rows = int(screen.height / resolution - 400 / resolution);
    createCanvas(cols * resolution, rows * resolution + 150);
    grid = make2DArray(cols, rows);
    age = make2DArray(cols, rows);
    for (let i = 0; i < cols; i++)
    {
        for (let j = 0; j < rows; j++)
        {
            grid[i][j] = floor(random(2));
            age[i][j] = 0;
        }
    }
    stroke(0);
    textSize(15);

    bottom = screen.height - 300;
    fSlider = createSlider(0, 0.0001, 0.00001, 0.000001);
    fSlider.position(20, bottom + 20);
    pSlider = createSlider(0, 0.01, 0.001, 0.0001);
    pSlider.position(20, bottom + 50);
    hSlider = createSlider(0, 1, 0.1, 0.01);
    hSlider.position(20, bottom + 80);
    mSlider = createSlider(0, 100, 50, 1);
    mSlider.position(20, bottom + 110);
}

function draw()
{
    background(0);
    f = fSlider.value();
    p = pSlider.value();
    h = hSlider.value();
    mature = mSlider.value();
    fill(255);
    text('Lightning chance', fSlider.x * 2 + fSlider.width, bottom - 72);
    text('Spawn chance', pSlider.x * 2 + pSlider.width, bottom - 42);
    text('Humidity', hSlider.x * 2 + hSlider.width, bottom - 12);
    text('Grow speed', mSlider.x * 2 + mSlider.width, bottom + 18);

    for (let i = 0; i < cols; i++)
    {
        for (let j = 0; j < rows; j++)
        {
            let x = i * resolution;
            let y = j * resolution;
            if(grid[i][j] == 1)
            {
                fill(0, 166, 0);
                rect(x, y, resolution-1, resolution-1);
            }
            if(grid[i][j] == 2)
            {
                fill(219, 0, 0);
                rect(x, y, resolution-1, resolution-1);
            }
            if(grid[i][j] == 3)
            {
                fill(128, 65, 25);
                rect(x, y, resolution-1, resolution-1);
            }
        }
    }

    let next = make2DArray(cols, rows);

    // Compute next based on grid
    for (let i = 0; i < cols; i++)
    {
        for (let j = 0; j < cols; j++)
        {
            let state = grid[i][j];

            // Check for neighbors


            if (state == 1)
            {
                let burning = burningNeighbor(grid, i, j);
                if((burning == true && Math.random() < (1 - h)) || Math.random() < f)
                {
                    next[i][j] = 2;
                }
                else
                {
                    next[i][j] = state;
                }
            } 
            else if (state == 2)
            {
                next[i][j] = 0;
            }
            else if (state == 0)
            {
                if (Math.random() < p)
                {
                    age[i][j] = 0;
                    next[i][j] = 3;
                }
                else
                {
                    next[i][j] = state;
                }
            }
            else if (state == 3)
            {
                age[i][j] += 0.1
                if (age[i][j] > mature)
                {
                    next[i][j] = 1;
                }
                else
                {
                    next[i][j] = state;
                }
            }
        }
    }
    grid = next;

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

function burningNeighbor(grid, x, y)
{
    let sum = 0;
    for (let i = -1; i < 2; i++)
    {
        for (let j = -1; j < 2; j++)
        {
            let col = (x + i + cols) % cols;
            let row = (y+ j + rows) % rows;
            let state = grid[col][row];
            if (state == 2)
            {
                return true;
            } 
        }
    }
}
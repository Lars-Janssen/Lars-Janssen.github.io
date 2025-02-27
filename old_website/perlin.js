let n = 2;
let height = 500;
let width = 500;
let fr = 30;
let resolution = 100;
let t = 0;

function setup()
{
    createCanvas(width, height);
    background(255);
    frameRate(fr);

    for (let i = 0; i < width; i++)
    {
        for (let j = 0; j < height; j++)
        {
            let value = round(noise(i / resolution,j / resolution, t)) * 255;
            stroke(value);
            strokeWeight(10);
            point(i,j);
        }
    }
}


function draw()
{
    t++;
    for (let i = 0; i < width; i++)
    {
        for (let j = 0; j < height; j++)
        {
            let value = round(noise(i / resolution,j / resolution, t)) * 255;
            stroke(value);
            strokeWeight(10);
            point(i,j);
        }
    }
}
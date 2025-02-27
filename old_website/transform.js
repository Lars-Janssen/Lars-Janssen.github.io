function makeline(point1x, point1y, point2x, point2y)
{
    line(point1x, point1y, point2x, point2y);
    vertexlist.push([point1x, point1y]);
    vertexlist.push([point2x, point2y]);
}

function multiplyMatrixAndPoint(matrix, point)
{
    // Give a simple variable name to each part of the matrix, a column and row number
    let c0r0 = matrix[ 0], c1r0 = matrix[ 1], c2r0 = matrix[ 2];
    let c0r1 = matrix[ 3], c1r1 = matrix[ 4], c2r1 = matrix[ 5];
    let c0r2 = matrix[ 6], c1r2 = matrix[ 7], c2r2 = matrix[ 8];
  
    // Now set some simple names for the point
    let x = point[0];
    let y = point[1];
    let w = point[2];
  
    // Multiply the point against each part of the 1st column, then add together
    let resultX = (x * c0r0) + (y * c0r1) + (w * c0r2);
  
    // Multiply the point against each part of the 2nd column, then add together
    let resultY = (x * c1r0) + (y * c1r1) + (w * c1r2);
  
    // Multiply the point against each part of the 3rd column, then add together
    let resultW = (x * c2r0) + (y * c2r1) + (w * c2r2);

  
    return [resultX, resultY, resultW];
}

function matrixmult(matrixB, matrixA)
{
    // Slice the second matrix up into rows
    let row0 = [matrixB[ 0], matrixB[ 1], matrixB[ 2]];
    let row1 = [matrixB[ 3], matrixB[ 4], matrixB[ 5]];
    let row2 = [matrixB[ 6], matrixB[ 7], matrixB[ 8]];

    // Multiply each row by matrixA
    let result0 = multiplyMatrixAndPoint(matrixA, row0);
    let result1 = multiplyMatrixAndPoint(matrixA, row1);
    let result2 = multiplyMatrixAndPoint(matrixA, row2);

    // Turn the result rows back into a single matrix

    return [
    result0[0], result0[1], result0[2],
    result1[0], result1[1], result1[2],
    result2[0], result2[1], result2[2],
    ];
}

function vectormult(matrix, vector)
{
    output = []
    for(let i = 0; i < matrix.length / 3; i++)
    {
        temp = 0
        for(let j = 0; j < vector.length; j++)
        {
            temp += matrix[i * 3 + j] * vector[j]
        }
        output.push(temp);
    }
    return output
}

function matrixadd(matrixA, matrixB)
{
    for(let i = 0; i < matrixA.length; i++)
    {
        for(let j = 0; j < matrixA[0].length; j++)
        {
            matrixA[i][j] += matrixB[i][j]
        }
    }

    return matrixA
}

function e2h(v)
{
    return [v[0], v[1], 1];
}

function h2e(v)
{
    if(v[2] != 0)
    {
    return [v[0] / v[2], v[1] / v[2]];
    }
    else
    {
        return 1;
    }
}


var vertexlist = []
var transformedlist = []
var inputs = new Array(9);

function setup()
{
    createCanvas(600, 500);
    background(255);
    angleMode(DEGREES);
    strokeWeight(1);
    line(width / 2, 0, width / 2, height);

    stroke('purple');

    makeline(100, 100, 100, 200);
    makeline(100, 200, 200, 200);
    makeline(200, 200, 200, 100);
    makeline(200, 100, 100, 100);

    inputs = new Array(9);
    var boxSize = 20;
    for(let i = 0; i < inputs.length; i++)
    {
        if(i == 0 || i == 4 || i == 8)
        {
            inputs[i] = createInput(1);
        }
        else
        {
            inputs[i] = createInput(0);
        }
        inputs[i].position(20 + (i % 3) * boxSize, 400 + (int(i / 3) % 3) * boxSize);
        inputs[i].size(boxSize,boxSize);
    }
}

angle = 0;
function draw()
{
    background(255);
    stroke('black');
    line(width / 2, 0, width / 2, height);
    stroke('purple');

    var transformation;
    var rotationpoint = [150, 150];

    var translationto0 = [1, 0, -rotationpoint[0], 0, 1, -rotationpoint[1], 0, 0, 1];
    var translationback = [1, 0, rotationpoint[0], 0, 1, rotationpoint[1], 0, 0, 1];

    var user = [inputs[0].value(), inputs[1].value(), inputs[2].value(),
                inputs[3].value(), inputs[4].value(), inputs[5].value(),
                inputs[6].value(), inputs[7].value(), inputs[8].value()];

    var translationfinal = [1,0,width / 2,
                   0,1,0,
                   0,0,1];
    

    transformation = matrixmult(user, translationto0);
    transformation = matrixmult(translationback, transformation);
    transformation = matrixmult(translationfinal, transformation);

    transformedlist = new Array(vertexlist.length);
    for(let i = 0; i < vertexlist.length; i++)
    {
        const original = e2h(vertexlist[i]);
        var transformedh = vectormult(transformation, original);
        const transformed = h2e(transformedh);
        if(transformed != 1)
        {
            transformedlist[i] = transformed;
        }
        else
        {
            transformedlist[i] = [0,0];
        }
    }

    for(let i = 0; i < transformedlist.length / 2; i++)
    {
        line(vertexlist[i * 2][0], vertexlist[i * 2][1], vertexlist[i * 2 + 1][0], vertexlist[i * 2 + 1][1]);
        line(transformedlist[i * 2][0], transformedlist[i * 2][1], transformedlist[i * 2 + 1][0], transformedlist[i * 2 + 1][1]);
    }
}

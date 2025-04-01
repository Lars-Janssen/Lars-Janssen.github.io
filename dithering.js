let img;
let blurredImg;


let colors = get_colors([[218, 215, 205], [163, 177, 138], [88, 129, 87], [58, 90, 64], [52, 78, 65]]);
console.log(colors);

function preload() {
    img = loadImage('image.jpg');
}

function setup() {
    for (let i = 0; i < colors.length; i++)
    {
        console.log(get_brightness(colors[i]));
    }
    createCanvas(2048*2, 2048*2);
    //img.filter(DILATE);
    img.resize(512, 512);
}

function get_index(x, y) {
    return (x + y * img.width) * 4;
}

function get_brightness(color)
{
    let brightness = 0.299 * color[0] + 0.587 *  color[1] + 0.114 *  color[2];
    return brightness;
}

function get_colors(colors)
{
    const array = [];

    for(let i = 0; i < colors.length; i++)
    {
        array[i] = colors[i];
    }

    // Sort by perceived brightness
    array.sort((a, b) => {
        let brightnessA = get_brightness(a);
        let brightnessB = get_brightness(b);
        return brightnessA - brightnessB;
    });

    return array;
}

function closest_color(old_color, gray, method) {
    if (gray) 
    {
        brightness = get_brightness(old_color);
        if (method)
            {
                let closest = colors[0];
                let dist = 10000;
                for (let i = 0; i < colors.length; i++)
                {
                    color_brightness = get_brightness(colors[i]);
                    let dr = old_color[0] - color_brightness;
                    let dg = old_color[1] - color_brightness;
                    let db = old_color[2] - color_brightness;
                    let liner = 1/2 * (old_color[0] + color_brightness);
                    let distToColor;

                    distToColor = sqrt((2 + liner/256) * dr ** 2 + 4 * dg ** 2 + (2 + (255-liner)/256) * db ** 2);

                    if (distToColor < dist)
                    {
                        dist = distToColor;
                        closest = colors[i];
                    }
                }
                return closest;
            } 
            else
            {
                let index = ceil(brightness / 255 * colors.length) - 1;
                index = index < 0 ? 0 : index;
                return [colors[index][0], colors[index][1], colors[index][2]];
            }
    }
    else
    {
        return colors.reduce((closest, color) => {
            let dr = old_color[0] - color[0];
            let dg = old_color[1] - color[1];
            let db = old_color[2] - color[2];
            let liner = 1/2 * (old_color[0] + color[0]);
            let distToColor;

            distToColor = sqrt((2 + liner/256) * dr ** 2 + 4 * dg ** 2 + (2 + (255-liner)/256) * db ** 2);
            return distToColor < closest.distance ? { color, distance: distToColor } : closest;
        }, { color: null, distance: Infinity }).color;
    }
    
}

function sharpen(img, factor = 10) {
    let sharpenedImg = img.get(); // Copy the image
    sharpenedImg.loadPixels();
    img.loadPixels();

    for (let y = 1; y < img.height - 1; y++) {
        for (let x = 1; x < img.width - 1; x++) {
            let index = get_index(x, y);
            let top = get_index(x, y - 1);
            let left = get_index(x - 1, y);
            let right = get_index(x + 1, y);
            let bottom = get_index(x, y + 1);

            for (let c = 0; c < 3; c++) { // Loop through R, G, B channels
                let center = img.pixels[index + c];
                let t = img.pixels[top + c];
                let l = img.pixels[left + c];
                let r = img.pixels[right + c];
                let b = img.pixels[bottom + c];

                // Unsharp mask formula: New pixel = (1 + factor) * center - factor * (surrounding pixels)
                let sharpened = (1 + factor) * center - factor * (t + l + r + b) / 4;

                // Clamp values to valid range [0, 255]
                sharpenedImg.pixels[index + c] = constrain(sharpened, 0, 255);
            }
        }
    }

    sharpenedImg.updatePixels();
    return sharpenedImg;
}


function dither(img, gray, method)
{
    let dimg = img.get(); // Copy the image
    dimg.loadPixels();

    let tallies = [0,0,0,0];
    for (let y = 0; y < dimg.height; y++)
    {
        for (let x = 0; x < dimg.width; x++)
        {
            let index = get_index(x, y);
            let old_r, old_g, old_b;
            if (gray)
            {
                old_r = get_brightness([dimg.pixels[index], dimg.pixels[index+1], dimg.pixels[index+2]]);
                old_g = old_r;
                old_b = old_r;
            } 
            else
            {
                old_r = dimg.pixels[index];
                old_g = dimg.pixels[index + 1];
                old_b = dimg.pixels[index + 2];
            }

            let new_c = closest_color([old_r, old_g, old_b], gray, method);
            let new_brightness = gray ? get_brightness(new_c): 0;
            
            dimg.pixels[index] = new_c[0];
            dimg.pixels[index + 1] = new_c[1];
            dimg.pixels[index + 2] = new_c[2];
            
            let err_r, err_g, err_b;
            if (gray)
            {
                err_r = old_r - new_brightness;
                err_g = old_g - new_brightness;
                err_b = old_b - new_brightness;
            } else
            {
                err_r = old_r - new_c[0];
                err_g = old_g - new_c[1];
                err_b = old_b - new_c[2];
            }
            
            if (x < dimg.width -1)
            {
            index = get_index(x + 1, y);
            dimg.pixels[index]     = dimg.pixels[index] + err_r * 7 / 16;
            dimg.pixels[index + 1] = dimg.pixels[index + 1] + err_g * 7 / 16;
            dimg.pixels[index + 2] = dimg.pixels[index + 2] + err_b * 7 / 16;
            }
            
            if (x > 0 & y < dimg.height - 1)
            {
            index = get_index(x - 1, y + 1);
            dimg.pixels[index]     = dimg.pixels[index] + err_r * 3 / 16;
            dimg.pixels[index + 1] = dimg.pixels[index + 1] + err_g * 3 / 16;
            dimg.pixels[index + 2] = dimg.pixels[index + 2] + err_b * 3 / 16;
            }
            
            if (y < dimg.height - 1)
            {
            index = get_index(x, y + 1);
            dimg.pixels[index]     = dimg.pixels[index] + err_r * 5 / 16;
            dimg.pixels[index + 1] = dimg.pixels[index + 1] + err_g * 5 / 16;
            dimg.pixels[index + 2] = dimg.pixels[index + 2] + err_b * 5 / 16;
            }

            if (x < dimg.width - 1 & y < dimg.height - 1)
            {
            index = get_index(x + 1, y + 1);
            dimg.pixels[index]     = dimg.pixels[index] + err_r * 1 / 16;
            dimg.pixels[index + 1] = dimg.pixels[index + 1] + err_g * 1 / 16;
            dimg.pixels[index + 2] = dimg.pixels[index + 2] + err_b * 1 / 16;
            }
        }
    }
    dimg.updatePixels();
    return dimg;
}

function grayscale(img)
{
    let gimg = img.get(); // Copy the image
    gimg.loadPixels();

    for (let y = 0; y < gimg.height; y++)
    {
        for (let x = 0; x < gimg.width; x++)
        {
            let index = get_index(x, y);
            let r = get_brightness([gimg.pixels[index], gimg.pixels[index+1], gimg.pixels[index+2]]);
            let g = r;
            let b = r;

            gimg.pixels[index]   = r;
            gimg.pixels[index+1] = g;
            gimg.pixels[index+2] = b;
        }
    }

    gimg.updatePixels();
    return gimg;
}

function draw() {
    image(img, 0, 0, 512, 512);
    image(dither(img, false), 512, 0, 512, 512);
    image(sharpen(img), 0, 512, 512, 512);
    image(dither(sharpen(img), false), 512, 512, 512, 512);
    image(grayscale(img), 0, 1024, 512, 512);
    image(dither(img, true, false), 512, 1024, 512, 512);
    image(grayscale(img), 0, 1536, 512, 512);
    image(dither(img, true, true), 512, 1536, 512, 512);
    image(grayscale(img), 0, 2048, 512, 512);
    image(dither(grayscale(img), true, true), 512, 2048, 512, 512);
    img_2 = dither(img, true, true);
    img_3 = dither(grayscale(img), true, true);
    //img_2.save();
    //img_3.save();
    noLoop();
}
// a shader variable
let theShader;

function preload(){
  // load the shader
  theShader = loadShader('shader.vert', 'shader.frag');
}

function setup() {
  // shaders require WEBGL mode to work
  createCanvas(windowWidth, windowHeight, WEBGL);

  tex1 = createGraphics(w, h, WEBGL);
  
  // Initialize the textures with random data
  tex1.background(0);
  tex1.fill(255);
  for (let x = 0; x < w; x += cellSize) {
    for (let y = 0; y < h; y += cellSize) {
      if (random(1) > 0.5) {
        tex1.rect(x, y, cellSize, cellSize);
      }
    }
  }
  noStroke();
}

function draw() {
  // shader() sets the active shader with our shader
  shader(theShader);

  // rect gives us some geometry on the screen
  theShader.setUniform("u_time", Math.sin(millis() / 1000.0));
  theShader.setUniform("u_tex", tex1);
  rect(0,0,width,height);
  
  // print out the framerate
  //  print(frameRate());
}

function windowResized(){
  resizeCanvas(windowWidth, windowHeight);
}

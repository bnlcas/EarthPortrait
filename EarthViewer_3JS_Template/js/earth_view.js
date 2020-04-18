var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1,100);

var renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

var camera_distance = 2;
var earth_radius = 1;
var sun_distance = 22;

var geometry = new THREE.SphereGeometry(earth_radius, 128, 128);
var texture = new THREE.TextureLoader().load( "Assets/earth_texture_map.jpg" );
var material = new THREE.MeshLambertMaterial({ map: texture});

var earth = new THREE.Mesh(geometry, material);
earth.rotation.x += 23.5 * Math.PI / 180
scene.add(earth);

//Lighting:
var light = new THREE.PointLight(0xFCFFDE, 1, 200);
light.position.set(0,0, sun_distance);
scene.add(light);

camera.position.set(0, 0, camera_distance);


function rotateAroundWorldAxis( object, axis, radians ) {

    var rotationMatrix = new THREE.Matrix4();

    rotationMatrix.makeRotationAxis( axis.normalize(), radians );
    rotationMatrix.multiplySelf( object.matrix );                       // pre-multiply
    object.matrix = rotationMatrix;
    object.rotation.setEulerFromRotationMatrix( object.matrix );
}

function RotateEarth(cycle_angle)
{
  //camera.up = new THREE.Vector3(0,1,0);
  //camera.lookAt(new THREE.Vector3(0,0,0));
  //earth.rotation.y += cycle_angle * Math.PI / 180
  var ang_rad = cycle_angle * Math.PI / 180;
  //rotateAroundWorldAxis(earth, new THREE.Vector3(0.1, 0.9, 0), ang_rad);
  earth.rotateOnWorldAxis(new THREE.Vector3(0, 1, 0), ang_rad);
}

var cycle_angle = 0.0;
var cycle_increment = 12;

function onDocumentKeyDown(event) {
    var keyCode = event.which;
    //console.log(keyCode);
    if (keyCode == 37) {
        RotateEarth(-cycle_increment);
    } else if (keyCode == 39) {
        RotateEarth(cycle_increment);
    }
    renderer.render(scene, camera);
};

renderer.render(scene, camera);
function animate()
{
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
  //cycle_angle += cycle_increment;
}
document.addEventListener("keydown", onDocumentKeyDown, false);
//animate();

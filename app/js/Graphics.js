var Graphics = function(id) {
    
    var element = document.getElementById(id);
    var context = element.getContext('2d');
    context.beginPath();
    context.strokeStyle = "#000000";
    context.lineWidth = 2;
    
    this.animate = function(drawMe) {
        drawArray[drawMe]();
    }
    
    
    var head = function() {
        context.beginPath();
        context.arc(60, 25, 10, 0, Math.PI * 2, true);
        context.stroke();
        context.closePath();
    }
    
    var draw = function($pathFromx, $pathFromy, $pathTox, $pathToy) {
        context.beginPath();
        context.moveTo($pathFromx, $pathFromy);
        context.lineTo($pathTox, $pathToy);
        context.stroke();
        context.closePath();
    }
    
    var frame1 = function() {
        draw(0, 150, 150, 150);
    };
    
    var frame2 = function() {
        draw(10, 0, 10, 600);
    };
    
    var frame3 = function() {
        draw(0, 5, 70, 5);
    };
    
    var frame4 = function() {
        draw(60, 5, 60, 15);
    };
    
    var torso = function() {
        draw(60, 36, 60, 70);
    };
    
    var rightArm = function() {
        draw(60, 46, 100, 50);
    };
    
    var leftArm = function() {
        draw(60, 46, 20, 50);
    };
    
    var rightLeg = function() {
        draw(60, 70, 100, 100);
    };
    
    var leftLeg = function() {
        draw(60, 70, 20, 100);
    };
    
    var drawArray = [rightLeg, leftLeg, rightArm, leftArm, torso, head, frame4, frame3, frame2, frame1];
    
    this.clear = function() {
        context.clearRect(0, 0, 400, 400);
    }
}
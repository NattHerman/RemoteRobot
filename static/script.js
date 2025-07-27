var socket = io();

// Clamped between -1 and 1
var speed = 0
// Clamped between -1 and 1
var turning = 0

// Stop robot when tab lost focus
window.addEventListener("blur", () => {
    speed = 0
    turning = 0
    console.log("Lost focus, stopping robot")
    socket.emit("robot_update", 0, 0)
})

addEventListener("keydown", (event) => {
    //console.log("down", event.key, "repeating", event.repeat)
    
    if (event.repeat) {
        return
    }

    switch(event.key) {
        case "w":
            speed += 1
            break;
        case "s":
            speed -= 1
            break;
        case "a":
            turning += 1
            break;
        case "d":
            turning -= 1
            break;
    }

    if ("wasd".includes(event.key)) {
        console.log(speed, turning)
        socket.emit("robot_update", speed, turning)
    }
})

addEventListener("keyup", (event) => {
    //console.log("up", event.key)
    
    switch(event.key) {
        case "w":
            speed -= 1
            break;
        case "s":
            speed += 1
            break;
        case "a":
            turning -= 1
            break;
        case "d":
            turning += 1
            break;
    }

    if ("wasd".includes(event.key)) {
        console.log(speed, turning)
        socket.emit("robot_update", speed, turning)
    }
})

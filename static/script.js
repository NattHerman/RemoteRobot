var socket = io();

// Clamped between -1 and 1
var speed = 0
// Clamped between -1 and 1
var turning = 0

var servoOffsetInputs = [
    document.getElementById("servo0"),
    document.getElementById("servo1"),
    document.getElementById("servo2"),
    document.getElementById("servo3"),
]

var setOffsetButton = document.getElementById("setOffsetButton")

function updateOffsets() {
    offsets = servoOffsetInputs.map((element) => { return Number(element.value) })

    console.log("offsets sent:", offsets)
    socket.emit("set_offsets", offsets)
}

// Update offsets when button pressed
setOffsetButton.addEventListener("click", updateOffsets)

// Also update when pressing enter in one of the input boxes
for (input of servoOffsetInputs) {
    input.addEventListener("change", updateOffsets)
}

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

// Set values of offset input to existing servo offsets 
socket.on("send_existing_offsets", (offsets) => {
    console.log("offsets recieved:", offsets)
    offsets.map((servoOffset, index) => {
        servoOffsetInputs[index].value = servoOffset
    })
})
var socket = io();

// Clamped between -1 and 1
var speed = 0
// Clamped between -1 and 1
var turning = 0


//      -- Updating servo offsets --

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

// On load and when values changed: Set values of offset input to server side servo offsets 
socket.on("send_existing_offsets", (offsets) => {
    console.log("offsets recieved:", offsets)
    offsets.map((servoOffset, index) => {
        servoOffsetInputs[index].value = servoOffset
    })
})

// Update offsets when button pressed
setOffsetButton.addEventListener("click", updateOffsets)

// Also update when setting value of the input boxes
for (input of servoOffsetInputs) {
    input.addEventListener("change", updateOffsets)
}

// Stop robot when tab lost focus
window.addEventListener("blur", () => {
    speed = 0
    turning = 0
    console.log("Lost focus, stopping robot")
    socket.emit("stop_robot")
})


//      -- Controlling the robot --

// Control using wasd on a keyboard
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

// Control using joystick on the page
var joystickContainer = document.getElementById("joystickContainer")
var joystick = document.getElementById("joystick")
var isDragging = false
var previousJoystickTimestamp = Date.now( )
var joystickEventInterval = 20

joystickContainer.addEventListener("pointerdown", (event) => {
    isDragging = true
    // Prevent pointer from interacting with other elements while joystick is being used
    joystickContainer.setPointerCapture(event.pointerId)
})

joystickContainer.addEventListener("pointerup", (event) => {
    isDragging = false
    joystickContainer.releasePointerCapture(event.pointerId)

    // Reset joystick
    joystick.style.left = `50%`
    joystick.style.top = `50%`

    // Stop robot
    socket.emit("stop_robot")
})

joystickContainer.addEventListener("pointermove", (event) => {
    if (!isDragging) { return }

    const rect = joystickContainer.getBoundingClientRect();
    let x = (event.clientX - (rect.x + rect.width/2)) / rect.width * 2
    let y = (event.clientY - (rect.y + rect.height/2)) / rect.height * 2

    const vectorLength = Math.sqrt(x**2 + y**2)

    // Restrict joystick
    if (vectorLength > 1) {
        x = x / vectorLength
        y = y / vectorLength
    }

    joystick.style.left = `${x * 50 + 50}%`
    joystick.style.top = `${y * 50 + 50}%`

    // Restrict update event frequency
    let now = Date.now()
    if (now - previousJoystickTimestamp > joystickEventInterval) {
        socket.emit("robot_update", -y, -x)
        previousJoystickTimestamp = now
    }
    
    event.stopPropagation()
})


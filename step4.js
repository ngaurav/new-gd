const fs = require('fs');
const fabric = require('fabric').fabric;
const path = require('path');

var config = require('./config.json');
const step1_output = JSON.parse(fs.readFileSync(config.step1_output_file));
const step3_output = JSON.parse(fs.readFileSync(config.step3_output_file));
const step4_response_folder = config.step4_output_folder;

fabric.nodeCanvas.registerFont('ttf_files/BreeSerif-Regular.ttf', {
    family: 'bree serif'
});
fabric.nodeCanvas.registerFont('ttf_files/Jersey10-Regular.ttf', {
    family: 'jersey'
});
fabric.nodeCanvas.registerFont('ttf_files/EBGaramond-Italic-VariableFont_wght.ttf', {
    family: 'garamond'
});
fabric.nodeCanvas.registerFont('ttf_files/Jacquard24-Regular.ttf', {
    family: 'jacquard'
});
fabric.nodeCanvas.registerFont('ttf_files/Oswald-VariableFont_wght.ttf', {
    family: 'oswald'
});
fabric.nodeCanvas.registerFont('ttf_files/Merriweather-Black.ttf', {
    family: 'merriweather'
});
fabric.nodeCanvas.registerFont('ttf_files/Shrikhand-Regular.ttf', {
    family: 'shrikhand'
});
fabric.nodeCanvas.registerFont('ttf_files/Eczar-VariableFont_wght.ttf', {
    family: 'eczar'
});
fabric.nodeCanvas.registerFont('ttf_files/Charm-Regular.ttf', {
    family: 'charm'
});
fabric.nodeCanvas.registerFont('ttf_files/RockSalt-Regular.ttf', {
    family: 'rock salt'
});
fabric.nodeCanvas.registerFont('ttf_files/DancingScript-VariableFont_wght.ttf', {
    family: 'dancing script'
});
fabric.nodeCanvas.registerFont('ttf_files/Pacifico-Regular.ttf', {
    family: 'pacifico'
});
fabric.nodeCanvas.registerFont('ttf_files/Caveat-VariableFont_wght.ttf', {
    family: 'caveat'
});
fabric.nodeCanvas.registerFont('ttf_files/IndieFlower-Regular.ttf', {
    family: 'indie flower'
});
fabric.nodeCanvas.registerFont('ttf_files/AmaticSC-Regular.ttf', {
    family: 'amatic sc'
});
fabric.nodeCanvas.registerFont('ttf_files/Kalam-Regular.ttf', {
    family: 'kalam'
});
fabric.nodeCanvas.registerFont('ttf_files/Allura-Regular.ttf', {
    family: 'allura'
});
fabric.nodeCanvas.registerFont('ttf_files/KaushanScript-Regular.ttf', {
    family: 'kaushan script'
});
fabric.nodeCanvas.registerFont('ttf_files/Aladin-Regular.ttf', {
    family: 'aladin'
});
fabric.nodeCanvas.registerFont('ttf_files/Condiment-Regular.ttf', {
    family: 'condiment'
});

const canvas = new fabric.Canvas('canvas', {
    width: step1_output['width'],
    height: step1_output['height']
});

// Function to create canvas and render elements
async function createCanvas() {
    // Read all URLs from the text file
    
    const urls = step3_output.images[1].urls;

    for (let i = 0; i < urls.length; i++) {
        // const url = 'file://'+__dirname+'/'+urls[i]
        const url = urls[i]
        console.log(url)
        await new Promise((resolve, reject) => {
            // fabric.util.loadImage(url, function (img) {
            fabric.Image.fromURL(url, function(img) { 
                img.scaleToWidth(step1_output['width'])
                img.scaleToHeight(step1_output['height'])

                // const group = new fabric.Group([img], {});
                canvas.add(img);

                canvas.renderAll();

                // Save JSON
                // const json = JSON.stringify(canvas);
                // console.log(json);

                // Check if the directory exists
                if (!fs.existsSync(step4_response_folder)) {
                    // If it doesn't exist, create it
                    fs.mkdirSync(step4_response_folder, { recursive: true });
                }
                
                // Save PNG
                const out = fs.createWriteStream(step4_response_folder + `/output${i + 1}.png`);
                const stream = canvas.createPNGStream();
                stream.pipe(out);
                out.on('finish', () => {
                    console.log(`PNG saved successfully as output${i + 1}.png.`);
                    resolve();
                });
            }, function (err) {
                console.log('Error loading image.');
                console.log(err);
                reject(err);
            });
            // Set the size of the canvas
            canvas.setDimensions({ width: 1024, height: 1024 });
        });
    }
};


function createDynamicText(text, left, top, width, height, fontFamily, fontWeight, fill, fontSize, fontStyle = 'normal') {
    // TODO: 
    // Textbox or Text or IText
    // fontFamily = 'Jersey'

    console.log("FONT FAMILY")
    console.log(fontFamily)

    if(fontSize <= 50){
        fontSize = fontSize + 24;
    }
    else{
        fontSize = fontSize + 16;
    }

    // console.log("INSIDE CREATE DYNAMIC TEXT")
    const textbox = new fabric.Text(text, {
        left: left,
        top: top,
        // width: width,
        // height: height,
        fontSize: fontSize,
        fontFamily: fontFamily,
        fontWeight: fontWeight,
        fill: fill,
        fontStyle: fontStyle,
        textAlign: 'center',
    });

    // Calculate the actual width of the text
    const textWidth = getTextWidth(text, fontFamily, fontWeight, fontSize);

    // Adjust the left position to center the text horizontally
    textbox.set({
        // fontSize: fontSize,
        left: left - (textWidth / 2)
    });

    return textbox;
}

function getTextWidth(text, fontFamily, fontWeight, fontSize) {
    const ctx = canvas.getContext("2d");
    ctx.font = fontWeight + " " + fontSize + "px " + fontFamily;
    const width = ctx.measureText(text).width;
    return width;
}

createCanvas();
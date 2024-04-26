const fs = require('fs');
const fabric = require('fabric').fabric;
const path = require('path');

var config = require('./config.json');
const step2_output = JSON.parse(fs.readFileSync(config.STEP2_OUTPUT_FILE));
const step3_response_file = config.STEP3_OUTPUT_FILE;

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

const poster_image = step2_output.poster_image

const canvas = new fabric.Canvas('canvas', {
    width: poster_image.width,
    height: poster_image.height
});

async function addImageToCanvas(url, width, height, x, y) {
    await new Promise((resolve, reject) => {
        fabric.Image.fromURL(url, function(img) { 
            img.scaleToWidth(width)
            img.scaleToHeight(height)
            img.left = x
            img.top = y
            resolve(img)    
        }, function (err) {
            console.log('Error loading image.');
            console.log(err);
            reject(err);
        });
        
    }).then ((result) => {
        canvas.add(result);
    });
}

async function addAssetToCanvas(asset_uri, width, height, x, y) {
    const src ='file://'+__dirname+'/'+config.INPUT_FOLDER+'/'+asset_uri
    await new Promise((resolve, reject) => {
        fabric.util.loadImage(src, function(asset) { 
            var img = new fabric.Image(asset)
            img.scaleToWidth(width)
            img.scaleToHeight(height)
            img.left = x
            img.top = y
            resolve(img);
        }, function (err) {
            console.log('Error loading image.');
            console.log(err);
            reject(err);
        });
    }).then ((result) => {
        canvas.add(result);
    });
}

// Function to create canvas and render elements
async function createCanvas() {
    // Add Background to Canvas
    await addImageToCanvas(poster_image.url, poster_image.width, poster_image.height, poster_image.x, poster_image.y)
    // Add all the foreground images to Canvas
    // for (let i = 0; i < step3_output.images.length; i++) {
    //     image = step3_output.images[i]
    //     await addImageToCanvas(image.urls[0], image.width, image.height, image.x, image.y)
    // }
    // Add all the assets to Canvas
    for (let i = 0; i < step2_output.assets.length; i++) {
        asset = step2_output.assets[i]
        await addAssetToCanvas(asset.asset_uri, asset.width, asset.height, asset.x, asset.y)
    }
    // Add all the texts to Canvas
    const textElements = step2_output.texts.map(t => {
        return createDynamicText(t.content, t.x, t.y, t.font_family, 'regular', "#FFFFFF", t.font_size, 'normal');
    })
    const group = new fabric.Group(textElements, {});//check
    canvas.add(group);
    // Render everything
    canvas.renderAll();
    
    // Save PNG
    const out = fs.createWriteStream(__dirname + '/' + step3_response_file);
    const stream = canvas.createPNGStream();
    stream.pipe(out);
    out.on('finish', () => {
        console.log(`PNG saved successfully.`);
    });
};


function createDynamicText(text, left, top, fontFamily, fontWeight, fill, fontSize, fontStyle = 'normal') {
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
    // textbox.set({
    //     // fontSize: fontSize,
    //     left: left - (textWidth / 2)
    // });

    return textbox;
}

function getTextWidth(text, fontFamily, fontWeight, fontSize) {
    const ctx = canvas.getContext("2d");
    ctx.font = fontWeight + " " + fontSize + "px " + fontFamily;
    const width = ctx.measureText(text).width;
    return width;
}

createCanvas();
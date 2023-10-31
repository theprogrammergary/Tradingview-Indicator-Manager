// // Function to convert a color value to RGB components
// function colorToRgb(color: string | null): { r: number; g: number; b: number } | null {
//     const tempElement = document.createElement("div");
//     tempElement.style.color = color!;
//     document.body.appendChild(tempElement);
//     const computedColor = window.getComputedStyle(tempElement).color;
//     document.body.removeChild(tempElement);

//     const matchRgb = computedColor.match(/\d+/g);
//     if (matchRgb) {
//         return {
//             r: parseInt(matchRgb[0]),
//             g: parseInt(matchRgb[1]),
//             b: parseInt(matchRgb[2]),
//         };
//     } else {
//         return null;
//     }
// }

// // Function to check if a color is within a tolerance range of #131722
// function isCloseTo131722(color: string | null, tolerance: number): boolean {
//     // Convert the color to RGB
//     const rgb = colorToRgb(color);

//     // Define the target RGB values for #131722
//     const targetR = 19;
//     const targetG = 23;
//     const targetB = 34;

//     // Calculate the differences between the target and actual RGB values
//     const diffR = Math.abs(targetR - rgb!.r);
//     const diffG = Math.abs(targetG - rgb!.g);
//     const diffB = Math.abs(targetB - rgb!.b);

//     // Check if all differences are within the specified tolerance
//     return diffR <= tolerance && diffG <= tolerance && diffB <= tolerance;
// }

// // Recursive function to change color styles to black when color is close to #131722
// function changeStylesToBlackWithTolerance(element: Node, tolerance: number) {
//     if (element.nodeType === Node.ELEMENT_NODE) {
//         // Check the computed styles for the element
//         const computedStyles = window.getComputedStyle(element as Element);

//         // Loop through computed styles and change colors to black when close to #131722
//         for (let i = 0; i < computedStyles.length; i++) {
//             const property = computedStyles[i];
//             const value = computedStyles.getPropertyValue(property);

//             // Check if the property contains "color" and the color is close to #131722
//             if (property.includes("color") && isCloseTo131722(value, tolerance)) {
//                 (element as HTMLElement).style.setProperty(property, "black", "important");
//             }
//         }
//     }

//     // Recursively process child elements
//     for (let i = 0; i < element.childNodes.length; i++) {
//         changeStylesToBlackWithTolerance(element.childNodes[i], tolerance);
//     }
// }

// // console.log("Content script loaded");

// console.log("Load event fired");
// changeStylesToBlackWithTolerance(document.body, 10);
// console.log("Changed Background to Black");


// document.addEventListener("load", function () {

//   console.log("Load event fired");
//   changeStylesToBlackWithTolerance(document.body, 10);
//   console.log("Changed Background to Black");


// });

// // console.log("Content script finished");


// function logStylesheets() {
//   const stylesheets = Array.from(document.styleSheets);

//   stylesheets.forEach((stylesheet, index) => {
//     console.log(`Stylesheet ${index + 1}: ${stylesheet.href || 'inline'}`);
//   });
// }

// // Call the function to log out stylesheets
// logStylesheets();

function replaceColorWithBlack(cssText: string): string {
    // Use regular expressions to find and replace color values
    const newCssText = cssText.replace(/#131722/g, '#000000');
    return newCssText;
}

document.addEventListener('copy', () => {

    console.log("Running extension")

    // Loop through all the stylesheets
    const stylesheets = Array.from(document.styleSheets);

    stylesheets.forEach((stylesheet) => {
        // Handle external stylesheets
        if (stylesheet.href) {
            // Fetch the stylesheet content
            fetch(stylesheet.href!)
                .then((response) => response.text())
                .then((cssText) => {
                    // Replace colors and update the stylesheet
                    const newCssText = replaceColorWithBlack(cssText);
                    const style = document.createElement('style');
                    style.textContent = newCssText;
                    document.head.appendChild(style);
                })
                .catch((error) => console.error(error));
        } else {
            // Handle inline stylesheets
            const cssText = (stylesheet.ownerNode as HTMLElement).textContent!;
            const newCssText = replaceColorWithBlack(cssText);
            (stylesheet.ownerNode as HTMLElement).textContent = newCssText;
        }
    });
});


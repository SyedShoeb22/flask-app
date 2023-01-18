from flask import Flask, request, jsonify, send_file
import cv2
import numpy as np
from rembg import remove
import requests

app = Flask(__name__)

@app.route('/process_image/<path:image_url>', methods=['GET'])
def process_image(image_url):
    response = requests.get(image_url)

# The response will contain the processed image in the form of bytes
    processed_image = response.content
    with open(r'temp.jpg', 'wb') as handler:
        handler.write(processed_image)   
    # Read image
    im = cv2.imread('temp.jpg')

    im = cv2.resize(im, dsize=(640, 640), fx=2, fy=2) # Resizing the image so that it fits on the cv2.imshow screen

    output = remove(im) # Removing background from cropped image
    cv2.imwrite('removed_bg.jpg', output)
    # Display cropped image
    #cv2.imwrite('croppedImg.jpg', im)

    img_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    canny = cv2.Canny(img_gray, 150, 255) # Applying canny egde detector to detect the edges of an image

    contours, hierarchy = cv2.findContours(image=canny, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE) # Finding contours
                                      
# draw contours on the original image
    image_copy = im.copy()
    img_highlighted = cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
      
    cv2.imwrite('contours_none_image1.jpg', image_copy)

    im = cv2.resize(im, dsize=(491, 516), fx=2, fy=2)
    cv2.imwrite( 'main.jpg', im)
    seg = cv2.resize(image_copy, dsize=(491, 516), fx=2, fy=2)
    cv2.imwrite( 'seg.jpg', seg)
    from PIL import Image, ImageFilter

    def drawContour(m,s,c,RGB):
        """Draw edges of contour 'c' from segmented image 's' onto 'm' in colour 'RGB'"""
        # Fill contour "c" with white, make all else black
        thisContour = s.point(lambda p:p==c and 255)
        

        # Find edges of this contour and make into Numpy array
        thisEdges   = thisContour.filter(ImageFilter.FIND_EDGES)
        thisEdgesN  = np.array(thisEdges)

        # Paint locations of found edges in color "RGB" onto "main"
        m[np.nonzero(thisEdgesN)] = RGB
        return m

    # Load segmented image as greyscale
    seg = Image.open(r"seg.jpg").convert('L')

    # Load main image - desaturate and revert to RGB so we can draw on it in colour
    main = Image.open(r"main.jpg").convert('L').convert('RGB')
    mainN = np.array(main)

    mainN = drawContour(mainN,seg,1,(255,0,0))   # draw contour 1 in red
    mainN = drawContour(mainN,seg,2,(255,255,0)) # draw contour 2 in yellow
    # Save result
    Image.fromarray(mainN).save('result.png')

    # Encode the processed image to send back in the response

    return send_file('result.png', mimetype='image/jpg')

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000,debug=True)

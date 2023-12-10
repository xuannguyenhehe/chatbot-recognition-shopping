import React, { useState, useEffect } from "react";
import { Image as Img } from "react-bootstrap";
import Resizer from "react-image-file-resizer";

const ImageLoad = React.memo(({ src, file, alt = "", size = 150 }) => {
  const [currentSrc, updateSrc] = useState(src);

  useEffect(() => {
    // start loading original image
    if(src !== ''){
      const imageToLoad = new Image();
      imageToLoad.src = src;
      if (file)
        Resizer.imageFileResizer(
          file,
          300,
          300,
          "JPEG",
          10,
          0,
          (uri) => {
            updateSrc(uri);
          },
          "base64",
          200,
          200
        );
    }
  }, [src, file]);

  return <Img src={currentSrc ? currentSrc : src} alt={alt} width={size} height={size} />;
});

export default ImageLoad;

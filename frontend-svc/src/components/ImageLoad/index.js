import React, { useState, useEffect } from "react";
import { Image as Img } from "react-bootstrap";
import Resizer from "react-image-file-resizer";

const ImageLoad = React.memo(({ src, placeholder, file, alt = "" }) => {
  const [currentSrc, updateSrc] = useState("http://dictionary.cambridge.org/vi/images/thumb/shirt_noun_002_33400.jpg?version=5.0.341");

  // useEffect(() => {
  //   // start loading original image
  //   if(src !== ''){
  //     const imageToLoad = new Image();
  //     imageToLoad.src = src;
  //     Resizer.imageFileResizer(
  //       file,
  //       300,
  //       300,
  //       "JPEG",
  //       10,
  //       0,
  //       (uri) => {
  //         updateSrc(uri);
  //       },
  //       "base64",
  //       200,
  //       200
  //     );
  //   }
  // }, [src, file]);

  return <Img src={currentSrc ? currentSrc : src} alt={alt} width="150" height="150" />;
});

export default ImageLoad;

// import ImagesUploading from "components/ImageUploading";
import ImageLoad from "components/ImageLoad";
import notification from "components/Notification";
import { useEffect, useState } from "react";
import { Card, Col, Container, Figure, Form, Row, Image } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import { useTranslation } from "react-i18next";
import ReactImagesUploading from "react-images-uploading";
import { useDispatch, useSelector } from "react-redux";
import { AiFillDelete } from "react-icons/ai";
import DragDropImage from "assets/maxresdefault.jpg";
import { convertBase64 } from "utils/base64";
import { getFullURL } from "utils/url";


const SettingImages = () => {
  const { t } = useTranslation();
  const image = useSelector((state) => state.image);
  const { uploadedImages } = image;
  const dispatch = useDispatch();

  useEffect(() => {
    if (!uploadedImages.length) {
      dispatch({
        type: "image/getUploadedImages",
      });
    }
  }, [uploadedImages]);

  const formatImageList = async (list, setList) => {
    let check = {};
    list.forEach(async (image) => {
      image.urls.forEach(async (image_url) => {
        const res = await fetch(getFullURL('image/' + image_url, "ENTRYPOINT"))
          .then(async (response) => {
            let contentType = response.headers.get("content-type");
            let blob = await response.blob();
            let imageName = image_url.split('/')[image_url.split('/').length - 1]
            imageName = image.label + '.' + imageName
            let file = new File([blob], imageName, { type: contentType });
            let base64 = await convertBase64(file).catch((e) => {
              notification("error", "[convertBase64] err" + e);
              check["unknow"] = true;
              return "";
            });
            return {
              data_url: base64,
              file: file,
            };
          })
          .catch((e) => {
            return {
              data_url: "",
              file: "",
            };
          });
          setList((prev) => {
            if (!prev.length) {
              return [{
                "label": image.label,
                "urls": [res],
              }]
            }
            else {
              let isFlagAddLabel = false;
              let isFlagUpdateLabel = false;
              let indexUpdateImageInLabel = null;
              prev.forEach((label, index) => {
                if (label.label === image.label) {
                  isFlagUpdateLabel = true;
                  indexUpdateImageInLabel = index;
                }
                else {
                  isFlagAddLabel = true;
                }
              })
              if (isFlagUpdateLabel) {
                let temp = prev.map((x) => x);
                temp[indexUpdateImageInLabel].urls.push(res);
                return [...temp];
              }
              else if (isFlagAddLabel) {
                return [...prev, {
                  "label": image.label,
                  "urls": [res],
                }]
              }
              return [...prev]
            }
          })
        });
    })
  }

  const [convertedUploadedImages, setConvertedUploadedImages] = useState([]);
  useEffect(() => {
    if (uploadedImages.length > 0) {
      formatImageList(uploadedImages, setConvertedUploadedImages);
    }
    // eslint-disable-next-line
  }, [uploadedImages]);

  const onChange = async (indexLabel, imageList) => {
    let temp = convertedUploadedImages.map((x) => x);
    temp[indexLabel].urls = imageList;
    setConvertedUploadedImages(temp);
  };

  const onUploadImage = () => {
    dispatch({
      type: "image/addNewUpload",
      payload: {
        images: convertedUploadedImages,
      },
    });
  };

  return (
    <Container className="p-2" style={{"maxWidth": "100%"}}>
      <Container className="d-flex justify-content-end" style={{"maxWidth": "100%"}}>
        <Button variant="warning">Change</Button>
        <Button variant="success" onClick={() => onUploadImage()}>Save</Button>
        <Button variant="danger">Cancel</Button>
      </Container>
      {convertedUploadedImages.length !== 0 && (
        <Container style={{"maxWidth": "100%"}}>
          {convertedUploadedImages.map((imageLabel, indexLabel) => {
            return (
            <Card className="my-2" style={{ border: "0px" }} key={indexLabel}>
              <Form.Group as={Row} className="m-2" controlId="formUploadName">
                <Col sm="3" className="pl-0">
                  <Form.Control
                    defaultValue={imageLabel.label}
                    disabled={true}
                  />
                </Col>
              </Form.Group>
              <Form>
              <ReactImagesUploading
                multiple
                value={imageLabel.urls}
                dataURLKey="data_url"
                onChange={(imageList) => onChange(indexLabel, imageList)}
              >
                {({
                      imageList,
                      onImageUpload,
                      onImageRemoveAll,
                      onImageUpdate,
                      onImageRemove,
                      isDragging,
                      dragProps,
                  }) => {
                    return (
                    <div className="p-2 m-2">
                      {imageList.length === 0 ? null : (
                          imageList.map((image, indexImageInLabel) => {
                            return (
                              <span
                                key={indexImageInLabel}
                                className="ml-2"
                              >
                                <Figure
                                  style={{ position: "relative", marginRight: "5px", border: "dashed 1px" }}
                                >
                                  <ImageLoad
                                    src={image.data_url}
                                    file={image.file}
                                  />
                                  <AiFillDelete
                                    className="icon-delete"
                                    size={20}
                                    onClick={() => onImageRemove(indexImageInLabel)}
                                    style={{
                                      "verticalAlign": "top",
                                      "color": "#ee0033",
                                      "position": "absolute",
                                      "cursor": "pointer",
                                      "top": 0,
                                      "right": 0,
                                    }}
                                  />
                                </Figure>
                              </span>
                            )
                          }
                        ))
                      }
                      <span 
                        className="ml-2"
                        {...dragProps}
                        onClick={onImageUpload}
                      >
                        <Figure style={{ position: "relative", marginRight: "5px", border: "dashed 1px" }}>
                          <Image src={DragDropImage} width="150" height="150" />
                        </Figure>
                      </span>
                    </div>
                  )}
                }
              </ReactImagesUploading>
              </Form>
          </Card>
          )})}
        </Container>
      )}
    </Container>
  );
};

export default SettingImages;

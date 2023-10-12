// import ImagesUploading from "components/ImageUploading";
import ImageLoad from "components/ImageLoad";
import notification from "components/Notification";
import { useCallback, useEffect, useState } from "react";
import { Card, Col, Container, Figure, Form, Row, Image } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
import { useTranslation } from "react-i18next";
import ReactImagesUploading from "react-images-uploading";
import { useSelector } from "react-redux";
import { AiFillDelete } from "react-icons/ai";
import DragDropImage from "assets/maxresdefault.jpg";


const SettingImages = () => {
  const { t } = useTranslation();
  const [batchName, setBatchName] = useState("Class");
  const image = useSelector((state) => state.image);
  // const { tempImages, uploadedImages } = image;
  const uploadedImages = [
    {
      "name": "shirt",
      "urls": [
        "http://dictionary.cambridge.org/vi/images/thumb/shirt_noun_002_33400.jpg?version=5.0.341",
        "http://dictionary.cambridge.org/vi/images/thumb/shirt_noun_002_33400.jpg?version=5.0.341",
        "http://dictionary.cambridge.org/vi/images/thumb/shirt_noun_002_33400.jpg?version=5.0.341",
        "http://dictionary.cambridge.org/vi/images/thumb/shirt_noun_002_33400.jpg?version=5.0.341",
        "http://dictionary.cambridge.org/vi/images/thumb/shirt_noun_002_33400.jpg?version=5.0.341",
      ]
    },
  ];

  const formatImageList = (list, setList) => {
    let check = {};
    list.forEach(async (image) => {
      image.urls = image.urls.map(async (image_url) => {
        // const res = await fetch(image_url)
        //   .then(async (response) => {
        //     let contentType = response.headers.get("content-type");
        //     let blob = await response.blob();
        //     let imageName = image_url.split('/')[image_url.split('/').length - 1]
        //     let file = new File([blob], imageName, { type: contentType });
        //     let base64 = await convertBase64(file).catch((e) => {
        //       notification("error", "[convertBase64] err" + e);
        //       check["unknow"] = true;
        //       return "";
        //     });
        //     return {
        //       data_url: base64,
        //       file: file,
        //     };
        //   })
        //   .catch((e) => {
        //     return {
        //       data_url: "",
        //       file: "",
        //     };
        //   });
        return "res";
      })
    })
    setList(list);
  };

  const [convertedUploadedImages, setConvertedUploadedImages] = useState([]);
  useEffect(() => {
    if (uploadedImages.length > 0) {
      formatImageList(uploadedImages, setConvertedUploadedImages);
    }
    // eslint-disable-next-line
  }, []);

  return (
    <Container className="p-2" style={{"maxWidth": "100%"}}>
      <Container className="d-flex justify-content-end" style={{"maxWidth": "100%"}}>
        <Button variant="warning">Change</Button>
        <Button variant="success">Save</Button>
        <Button variant="danger">Cancel</Button>
      </Container>
      {convertedUploadedImages.length !== 0 && (
        <Container style={{"maxWidth": "100%"}}>
          {convertedUploadedImages.map((image, index) => (
            <Card className="my-2" style={{ border: "0px" }} key={index}>
              <Form.Group as={Row} className="m-2" controlId="formUploadName">
                <Col sm="3" className="pl-0">
                  <Form.Control
                    defaultValue={image.name}
                    disabled={true}
                  />
                </Col>
              </Form.Group>
              <Form>
              <ReactImagesUploading
                multiple
                value={image.urls}
                dataURLKey="data_url"
              >
                {({
                      imageList,
                      onImageUpload,
                      onImageRemoveAll,
                      onImageUpdate,
                      onImageRemove,
                      isDragging,
                      dragProps,
                  }) => (
                    <div className="p-2 m-2">
                      {image.urls.length === 0 ? null : (
                          imageList.map((image, index) => {
                            return (
                              <span
                                key={index}
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
                                    onClick={null}
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
                  )
                }
              </ReactImagesUploading>
              </Form>
          </Card>
          ))}
        </Container>
      )}
    </Container>
  );
};

export default SettingImages;

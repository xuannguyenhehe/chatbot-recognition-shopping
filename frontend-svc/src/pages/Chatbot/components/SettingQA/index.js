import DragDropImage from "assets/maxresdefault.jpg";
import ImageLoad from "components/ImageLoad";
import notification from "components/Notification";
import i18n from "i18n";
import { useEffect, useState } from "react";
import { Card, Col, Container, Figure, Form, Image, Row } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
// import { useTranslation } from "react-i18next";
import { AiFillDelete } from "react-icons/ai";
import ReactImagesUploading from "react-images-uploading";
import { useDispatch, useSelector } from "react-redux";
import { convertBase64 } from "utils/base64";
import { getFullURL } from "utils/url";

const SettingQA = () => {
  // const { t } = useTranslation();
  const image = useSelector((state) => state.image);
  const { uploadedImages, isUploadAction } = image;
  const dispatch = useDispatch();

  useEffect(() => {
    if (!uploadedImages.length) {
      dispatch({
        type: "image/getUploadedImages",
      });
    }
  }, [dispatch, uploadedImages.length]);

  const formatImageList = async (list, setList) => {
    let check = {};
    setList([]);
    list.forEach(async (image) => {
      image.urls.forEach(async (image_url, image_index) => {
        const res = await fetch(getFullURL('image/' + image_url, "ENTRYPOINT"))
          .then(async (response) => {
            let contentType = response.headers.get("content-type");
            let blob = await response.blob();
            let imageName = image_url.split('/')[image_url.split('/').length - 1]
            imageName = image.ids[image_index] + '.' + image.label + '.' + imageName
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
                "stocking": image.stocking,
                "description": image.description,
                "urls": [res],
                "isModified": image.isModified,
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
                  "stocking": image.stocking,
                  "description": image.description,
                  "urls": [res],
                  "isModified": image.isModified,
                }]
              }
              return [...prev]
            }
          })
        });
    })
  }

  const [convertedUploadedImages, setConvertedUploadedImages] = useState([]);
  const [convertedTempImages, setConvertedTempImages] = useState([]);
  const [deletedImageIds, setDeletedImageIds] = useState([]);
  const [showImages, setShowImages] = useState([]);

  useEffect(() => {
    if (uploadedImages.length > 0) {
      formatImageList(uploadedImages, setConvertedUploadedImages);
    }
    // eslint-disable-next-line
  }, [uploadedImages]);

  useEffect(() => {
    if (isUploadAction) {
      setShowImages(convertedTempImages);
    } else {
      setShowImages(convertedUploadedImages);
      setConvertedTempImages(convertedUploadedImages)
    }
  }, [isUploadAction, convertedTempImages, convertedUploadedImages])

  const getIdsFromImages = (images) => {
    let imageNames = images.map(image => image.file.name);
    let ids = imageNames.filter(name => name.split('.').length >= 4).map(name => name.split('.')[0])
    return ids
  }

  const getDeleteImages = (oldImages, newImages) => {
    let oldIds = getIdsFromImages(oldImages);
    let existIds = getIdsFromImages(newImages);
    let differenceIds = oldIds.filter((element) => !existIds.includes(element)); 
    return differenceIds;
  }

  const onChange = async (indexLabel, imageList) => {
    let temp = convertedTempImages.map((x) => x);
    let differenceIds = getDeleteImages(temp[indexLabel].urls, imageList)
    if (differenceIds.length > 0) {
      setDeletedImageIds([...deletedImageIds, ...differenceIds])
    } 

    temp[indexLabel].urls = imageList;
    temp[indexLabel].isModified = true;
    setConvertedTempImages(temp);
  };

  const onAddNewLabel = () => {
    let temp = convertedTempImages.map((x) => x);
    temp.push({
      "label": "",
      "stocking": 0,
      "description": "",
      "urls": [],
      "isModified": true,
    })
    setConvertedTempImages(temp);
  }

  const onUploadImage = () => {
    dispatch({
      type: "image/addNewUpload",
      payload: {
        images: convertedTempImages,
        deletedImageIds: deletedImageIds,
      },
    });
  };

  const onChangeLabel = (indexLabel, type, event) => {
    let temp = convertedTempImages.map((x) => x);
    let newImageName = event.target.value;
    let imageAvailableNames = temp.map((image) => image[type]);
    if (imageAvailableNames.includes(newImageName) && type === "label") {
      notification("error", i18n.t("notify.failExistLabelName"));
    } else {
      temp[indexLabel][type] = type !== "stocking" ? event.target.value : parseInt(event.target.value);
      temp[indexLabel].isModified = true;
      setConvertedTempImages(temp);
    }
  }

  const onClickChangeBtn = () => {
    dispatch({
      type: "image/changeIsUploadAction",
    });
  }

  return (
    <Container className="p-2" style={{"maxWidth": "100%"}}>
      <Row>
        <Col sm={3}>
            {isUploadAction && (
                <Button 
                  variant="warning" 
                  onClick={() => onAddNewLabel()}
                  className="mx-2"
                >Add new label</Button>
            )}
        </Col>
        <Col sm={9} className="d-flex justify-content-end">
            {!isUploadAction && (
              <Button 
                variant="warning" 
                onClick={() => onClickChangeBtn()}
                className="mx-2"
              >Change</Button>
            )}
            {!isUploadAction && (
              <Button 
                variant="danger" 
                onClick={null}
                className="mx-2"
              >Train</Button>
            )}
            {isUploadAction && (
              <Button 
                variant="success" 
                onClick={() => onUploadImage()}
                className="mx-2"
              >Save</Button>
            )}
            {isUploadAction && (
              <Button 
                variant="danger" 
                onClick={() => onClickChangeBtn()}
                className="mx-2"
              >Cancel</Button>
            )}
        </Col>
      </Row>

      {showImages.length !== 0 && (
        <Container style={{"maxWidth": "100%"}}>
          {showImages.map((imageLabel, indexLabel) => {
            return (
            <Card className="my-2" style={{ border: "0px" }} key={indexLabel}>
              <Form.Group as={Row} className="m-2" controlId="formUploadName">
                <Row className="my-1">
                  <Col sm="3" className="pl-0">
                    <Form.Control
                      defaultValue={imageLabel.label}
                      onChange={(event) => onChangeLabel(indexLabel, "label", event)}
                      disabled={!isUploadAction}
                    />
                  </Col>
                  <Col sm="1" className="pl-0">
                    <Form.Control
                      defaultValue={imageLabel.stocking}
                      onChange={(event) => onChangeLabel(indexLabel, "stocking", event)}
                      disabled={!isUploadAction}
                    />
                  </Col>
                </Row>
                <Row className="my-1">
                  <Col sm="4" className="pl-0">
                    <Form.Control
                      as="textarea" rows={3}
                      defaultValue={imageLabel.descripton}
                      onChange={(event) => onChangeLabel(indexLabel, "description", event)}
                      disabled={!isUploadAction}
                      placeholder="Description of clothes"
                    />
                  </Col>
                </Row>
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
                                  {isUploadAction && (<AiFillDelete
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
                                  />)}
                                </Figure>
                              </span>
                            )
                          }
                        ))
                      }
                      {isUploadAction && (<span 
                        className="ml-2"
                        {...dragProps}
                        onClick={onImageUpload}
                      >
                        <Figure style={{ position: "relative", marginRight: "5px", border: "dashed 1px" }}>
                          <Image src={DragDropImage} width="150" height="150" />
                        </Figure>
                      </span>)}
                    </div>
                  )}
                }
              </ReactImagesUploading>
              </Form>
              {isUploadAction && (<AiFillDelete
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
              />)}
          </Card>
          )})}
        </Container>
      )}
    </Container>
  );
};

export default SettingQA;

import defaultAvatar from "assets/DefaultAvatar.png";
import ImageNotAvailable from "assets/Image_not_available.jpeg";
import loading from "assets/loader.gif";
import ImageLoad from "components/ImageLoad";
import notification from "components/Notification";
import ChatInput from "pages/Chat/components/ChatInput";
import { useCallback, useEffect, useRef, useState } from "react";
import { Button, Col, Container, Figure, Image, Modal, Row } from "react-bootstrap";
import ImageUploading from "react-images-uploading";
import { useDispatch, useSelector } from "react-redux";
import { v4 as uuidv4 } from "uuid";


const ChatContainer = ({ currentChatUser, messages }) => {
  const account = useSelector((state) => state.account);
  const  { username } = account;

  const isShowLoading = useSelector((state) => state.message.isShowLoading);
  const isLoading = useSelector((state) => state.message.isLoading);
  const currentMessage = useSelector((state) => state.message.currentMessage);
  const backupMessage = useSelector((state) => state.message.backupMessage);
  const currentImage = useSelector((state) => state.message.currentImage);
  const backupImage = useSelector((state) => state.message.backupImage);
  const currentOptions = useSelector((state) => state.message.currentOptions);
  const isShowImageUploadArea = useSelector((state) => state.message.isShowImageUploadArea);

  const [choseOptionImage, setChoseOptionImage] = useState(null);
  const [isShowImageOptionModal, setIsShowImageOptionModal] = useState(false);
  const [isShowMoreImageOptionModal, setIsShowMoreImageOptionModal] = useState(false);

  const dispatch = useDispatch();
  const scrollRef = useRef(null);

  const handleChangeImage = useCallback((image) => {
    dispatch({
      type: "message/saveState",
      payload: {
        currentImage: image,
      },
    });
  }, [dispatch])

  const handleIsShowImageUploadArea = useCallback((isShow) => {
    dispatch({
      type: "message/saveState",
      payload: {
        isShowImageUploadArea: isShow,
      },
    });
  }, [dispatch])

  const handleCurrentOptions = useCallback((currentOptions) => {
    dispatch({
      type: "message/saveState",
      payload: {
        currentOptions: currentOptions,
      },
    });
  }, [dispatch])

  const onChangeCurrentImage = (imageList) => {
    imageList.forEach((element) => {
      if (element.dataURL) {
        handleChangeImage(element)
        handleIsShowImageUploadArea(false)
      }
    });
  };

  const handleError = (errors, _) => {
    console.log(errors);
  };

  useEffect(() => {
    scrollRef.current?.scrollIntoView({ 
      behavior: "smooth",
      inline: "end",
    });
  }, [messages]);

  const handleSendMessage = async (msg, image, isForceSend) => {
    dispatch({
      type: "message/sendMessage",
      payload: {
        message: msg,
        chatUser: currentChatUser,
        image: image,
        isForceSend: isForceSend,
      },
    });
  };

  const handleSendChoseImageMessage = async (pathImage) => {
    dispatch({
      type: "message/sendChoseImageMessage",
      payload: {
        chatUser: currentChatUser,
        pathImage: pathImage,
      },
    });
    setIsShowImageOptionModal(false);
    handleCurrentOptions(null);
  };

  const handleSendSpecifiedMessage = async (message) => {
    dispatch({
      type: "message/sendSpecifiedMessage",
      payload: {
        chatUser: currentChatUser,
        message: message,
      },
    });
    setIsShowImageOptionModal(false);
  };

  const handleCreateNewChat = async (chatUser) => {
    dispatch({
      type: "chat/createNewChat",
      payload: {
        sender: username,
        receiver: chatUser,
      },
    });
  };

  const onMouseEnter = (e) => {
    e.target.style.border = '3px solid green';
    e.target.style.cursor = 'pointer';
  }
  const onMouseLeave = (e) => {
    e.target.style.border = '1px solid';
    e.target.style.cursor = '';
  }

  return (
    <Container>
      <Row className="mb-2">
          <Col sm={1} style={{"width": "5%"}}>
            <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
          </Col>
          <Col sm={10}>
            <h3 className="m-0 p-1">{currentChatUser}</h3>
          </Col>
      </Row>
      <Row>
      <hr/>
      {isShowLoading ? (
        <Col style={{"textAlign": "center",}}>
          <img 
            src={loading} 
            alt="loader" 
            style={{
              "width": "120px", 
              "height": "120px",
            }}
          />
        </Col>
      ) : <Container style={{
            "height": "70vh",
            "overflow": "auto",
          }}>
          {messages !== null && messages.map((message, indexMessage) => {
            return (
              <div 
                ref={scrollRef} 
                key={uuidv4()} 
                className={username !== message.sender ? "d-flex flex-row my-2" : "d-flex flex-row-reverse my-2"}
              >
                <Col sm={1} style={{"width": "6%"}} className="mx-2">
                  <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
                </Col>
                <Col sm={8} style={username === message.sender ? {"textAlign": "end"} : null}>
                  <p className="m-0" style={{"fontWeight": "bold"}}>{username !== message.sender ? currentChatUser : username}</p>
                  {message.image && (
                    <ImageLoad 
                      src={message.image}
                    />
                  )}
                  {message.message && (
                    <p>{message.message}</p>
                  )}
                  {message.options !== null && message.options?.length && message.options.map((option, indexOption) => {
                    return (
                      <Figure
                        key={indexOption}
                        style={{ 
                          position: "relative", 
                          marginRight: "5px", 
                          border: "1px solid",
                        }}
                        onMouseEnter={message.is_option_action && indexMessage === messages.length - 1 ? onMouseEnter: null}
                        onMouseLeave={onMouseLeave}
                        onClick={() => {
                          if (indexMessage === messages.length - 1) {
                            if (option.startsWith("http")) {
                              setChoseOptionImage(option)
                              setIsShowImageOptionModal(true)
                            } else {
                              handleSendSpecifiedMessage("Cảm ơn bạn đã quan tâm đến shop!")
                            }
                          }
                        }}
                      >
                        {option.startsWith("http") ? (
                          <ImageLoad 
                            src={option}
                          />
                        ) : option}
                      </Figure>
                    )})
                  }
                  {message.options !== null && message.options?.length && message.options[0].startsWith("http") && (<Figure 
                    style={{ 
                      position: "relative", 
                      marginRight: "5px", 
                    }}
                    onMouseEnter={message.is_option_action && indexMessage === messages.length - 1 ? onMouseEnter: null}
                    onMouseLeave={onMouseLeave}
                    onClick={() => {
                      setIsShowMoreImageOptionModal(true);
                    }}
                  >
                    <Image src={ImageNotAvailable} width="150" height="150" />
                  </Figure>)}
                </Col>
              </div>
            );
          })}
          {isLoading && (
            <Row className="d-flex flex-row">
              <Col sm={1} style={{"width": "5%"}}>
                <img src={defaultAvatar} alt="current Chat avatar" style={{"height": "3.1rem"}} />
              </Col>
              <Col sm={8}>...</Col>
            </Row>
          )}
        </Container>}
      </Row>

      <Modal show={isShowImageUploadArea}>
        <Modal.Header closeButton>
          <Modal.Title>Bạn có ảnh mẫu không?</Modal.Title>
        </Modal.Header>
        <Modal.Body>
            Việc có ảnh mẫu sẽ giúp chatbot tìm kiếm ảnh phù hợp nhất với bạn?
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => {
            handleIsShowImageUploadArea(false);
            handleSendMessage(currentMessage, currentImage, true)
          }}>
            Không
          </Button>
          <ImageUploading
            multiple={false}
            value={currentImage}
            onChange={onChangeCurrentImage}
            onError={handleError}
          >
            {({ onImageUpload }) => (
              <div>
                <Button variant="primary" onClick={onImageUpload}>Có</Button>
              </div>
            )}
          </ImageUploading>
        </Modal.Footer>
      </Modal>

      <Modal show={isShowImageOptionModal}>
        <Modal.Header closeButton>
          <Modal.Title>Ảnh này làm bạn hài lòng chứ?</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{"alignSelf": "center"}}>
          <ImageLoad 
            src={choseOptionImage}
            size={200}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => {
            notification("warning", "Bạn vui lòng chọn ảnh khác giúp mình nhé!");
            setIsShowImageOptionModal(false);
          }}>
            Không
          </Button>
          <Button variant="secondary" onClick={() => handleSendChoseImageMessage(choseOptionImage)}>
            Có
          </Button>
        </Modal.Footer>
      </Modal>

      <Modal show={isShowMoreImageOptionModal}>
        <Modal.Header closeButton>
          <Modal.Title>Bạn có muốn tìm kiếm ảnh khác không</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Chatbot sẽ tìm kiếm cho bạn những tấm ảnh phù hợp khác!
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => {
              setIsShowMoreImageOptionModal(false);
              handleSendSpecifiedMessage("Cảm ơn bạn đã quan tâm đến shop!")
              handleCurrentOptions(null);
            }}
          >
            Không
          </Button>
          <Button variant="secondary" onClick={() => {
              setIsShowMoreImageOptionModal(false);
              if (currentOptions && currentOptions.length < 5) {
                handleSendSpecifiedMessage("Rất tiếc shop không còn sản phẩm nào phù hợp với bạn. Bạn vui lòng đổi yêu cầu khác!")
                handleCurrentOptions(null);
              } else {
                dispatch({
                  type: "message/sendMessage",
                  payload: {
                    message: backupMessage,
                    chatUser: currentChatUser,
                    image: backupImage,
                    isForceSend: true,
                    isBackup: true,
                    offsetImage: currentOptions.length,
                  },
                });
              }
            }}
          >
            Có
          </Button>
        </Modal.Footer>
      </Modal>

      <ChatInput 
        handleSendMessage={handleSendMessage} 
        messages={messages} 
        chatUser={currentChatUser}
        handleCreateNewChat={handleCreateNewChat}
      />
    </Container>
  );
};

export default ChatContainer;

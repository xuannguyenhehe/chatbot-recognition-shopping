import cameraImage from "assets/camera.png";
import ImageLoad from "components/ImageLoad";
import Picker, { Theme } from "emoji-picker-react";
import { useState, useCallback } from "react";
import Button from 'react-bootstrap/Button';
import { AiFillDelete } from "react-icons/ai";
import { BsEmojiSmileFill } from "react-icons/bs";
import { IoMdSend } from "react-icons/io";
import ImageUploading from "react-images-uploading";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";


const ChatInput = ({ handleSendMessage, messages, chatUser, handleCreateNewChat}) => {
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const dispatch = useDispatch();

  const currentMessage = useSelector((state) => state.message.currentMessage);
  const currentImage = useSelector((state) => state.message.currentImage);

  const handleEmojiPickerhideShow = () => {
    setShowEmojiPicker(!showEmojiPicker);
  };

  const handleEmojiClick = (emojiObject, event) => {
    let message = currentMessage;
    message += emojiObject.emoji;
    handleChangeMessage(message);
  };

  const sendChat = (event) => {
    event.preventDefault();
    if (currentMessage.length > 0) {
      if (currentImage) {
        handleSendMessage(currentMessage, currentImage, true);
      } else{
        handleSendMessage(currentMessage, currentImage, false);
      }
    }
  };  

  const handleChangeMessage = useCallback((message) => {
    dispatch({
      type: "message/saveState",
      payload: {
        currentMessage: message,
      },
    });
  }, [dispatch])

  const handleChangeImage = useCallback((image) => {
    dispatch({
      type: "message/saveState",
      payload: {
        currentImage: image,
      },
    });
  }, [dispatch])

  const onChange = (imageList) => {
    imageList.forEach((element) => {
      if (element.dataURL) {
        handleChangeImage(element)
      }
    });
  };

  const handleError = (errors, _) => {
    console.log(errors);
  };

  if (messages !== null)
    return (
      <Container>
        <div className="button-container">
          <div className="emoji">
            <BsEmojiSmileFill onClick={handleEmojiPickerhideShow} />
            {showEmojiPicker && (
              <div className="emoji-picker-react">
                <Picker onEmojiClick={handleEmojiClick} theme={Theme.DARK} />
              </div>
            )}
          </div>
        </div>
        <form className="input-container" onSubmit={(event) => sendChat(event)}>
          <Container 
            style={{
              "position": currentImage ? "relative" : null, 
              "width": "90%",
              "height": currentImage ? "170px" : "50px",
              "backgroundColor": "#ffffff34",
              "borderRadius": "2rem",
            }} className="m-0 p-0">
            <input
              type="text"
              placeholder="type your message here"
              onChange={(e) => handleChangeMessage(e.target.value)}
              value={currentMessage}
              style={{
                "position": currentImage ? "absolute" : null, 
                "bottom": currentImage ? "1rem": null,
              }}
            />
            {currentImage ? 
              <span style={{
                  "position": "absolute",
                  "top": "-0.5rem",
                }} className="m-3">
                <ImageLoad src={currentImage.dataUrl} file={currentImage.file} size={100}/>
                <AiFillDelete
                  className="icon-delete"
                  size={20}
                  onClick={() => handleChangeImage(null)}
                  style={{
                    "verticalAlign": "top",
                    "color": "#ee0033",
                    "position": "absolute",
                    "cursor": "pointer",
                    "top": 0,
                    "right": 0,
                  }}
                />
              </span> : null}
          </Container>

          <button type="submit">
            <IoMdSend />
          </button>
        </form>
        <div className="image-send">
          <ImageUploading
            multiple={false}
            value={currentImage}
            onChange={onChange}
            onError={handleError}
          >
            {({ onImageUpload, isDragging, dragProps }) => (
              <div className="upload__image-wrapper">
                <button
                  style={isDragging ? { color: "red" } : undefined}
                  className="add-image-btn"
                  onClick={onImageUpload}
                  {...dragProps}
                >
                  <img src={cameraImage} alt="camera" />
                </button>
              </div>
            )}
          </ImageUploading>
        </div>
      </Container>
    );
  else 
    return (
      <Container>
        <Button 
          type="submit"
          style={{"width": "100%"}}
          onClick={() => handleCreateNewChat(chatUser)}
        >
          Subcribe
        </Button>
      </Container>
    );
};

const Container = styled.div`
  /* display: grid; */
  align-items: center;
  /* grid-template-columns: 15% 70% 15%; */
  background-color: #00000076;
  border-top: 0.2px solid #ffffff15;
  display: flex;
  padding: 0 2rem;
  justify-content: space-between;
  align-content: space-between;
  @media screen and (min-width: 590px) {
    /* grid-template-columns: 10% 90%; */
  }
  @media screen and (min-width: 1000px) {
    /* grid-template-columns: 5% 95%; */
    /* gap: 0.5rem; */
  }
  .button-container {
    display: flex;
    align-items: center;
    color: white;
    padding-right: 1rem;
    .emoji {
      position: relative;
      svg {
        font-size: 1.5rem;
        color: #ffff00c8;
        cursor: pointer;
      }
      .emoji-picker-react {
        position: absolute;
        top: -470px;
        border-color: #9a86f3;
        border-radius: 5%;
        .emoji-scroll-wrapper::-webkit-scrollbar {
          background-color: #080420;
          width: 5px;
          &-thumb {
            background-color: #9a86f3;
          }
        }
        .emoji-categories {
          button {
            filter: contrast(0);
          }
        }
        .emoji-search {
          background-color: transparent;
          border-color: #9a86f3;
        }
        .emoji-group:before {
          background-color: #080420;
        }
      }
    }
  }
  .input-container {
    width: 100%;
    border-radius: 2rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    /* background-color: #ffffff34; */
    input {
      width: 90%;
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 2rem;

      font-size: 1.1rem;
      background-color: transparent;
      &::selection {
        background-color: #9a86f3;
      }
      &:focus {
        outline: none;
      }
    }

    button {
      padding: 0.1rem 0.1rem;
      border-radius: 2rem;
      display: flex;
      justify-content: center;
      align-items: center;
      background-color: transparent;
      border: none;
      @media screen and (min-width: 720px) {
        padding: 0.2rem 0.2rem;

        svg {
          font-size: 1rem;
        }
      }
      svg {
        font-size: 2rem;
        color: rgb(0, 135, 255);
      }
    }
  }
  .image-send {
    .add-image-btn {
      color: white;
      background: transparent;
      outline: none;
      border: none;
      padding-left: 0.6rem;
      cursor: pointer;
      img {
        width: 2rem;
        height: 2rem;
      }
    }
  }
`;

export default ChatInput;

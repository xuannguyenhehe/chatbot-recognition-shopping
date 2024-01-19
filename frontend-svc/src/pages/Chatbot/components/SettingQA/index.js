import notification from "components/Notification";
import i18n from "i18n";
import { useEffect, useState } from "react";
import { Card, Col, Container, Form, Row } from "react-bootstrap";
import Button from 'react-bootstrap/Button';
// import { useTranslation } from "react-i18next";
import { AiFillDelete } from "react-icons/ai";
import { useDispatch, useSelector } from "react-redux";

const SettingQA = () => {
  // const { t } = useTranslation();
  const qa = useSelector((state) => state.qa);
  const { intents, isUploadAction, statusTrain } = qa;
  const [showIntents, setIntents] = useState([]);
  const dispatch = useDispatch();

  useEffect(() => {
    if (!intents.length) {
      dispatch({
        type: "qa/getAdditionalIntents",
      });
    } 
    
    if (!showIntents.length){
      setIntents(intents);
    }
  }, []);

  useEffect(() => {
    if (!statusTrain) {
      dispatch({
        type: "qa/checkStatusTrain",
      });
    }
  }, [statusTrain, dispatch])

  const onAddNewLabel = () => {
    let temp = showIntents.map((x) => x);
    temp.push({
      "questions": "",
      "answer": '',
      "keyword": "",
      "isModified" : true,
    })
    setIntents(temp);
  }

  const onChangeLabel = (indexLabel, type, event) => {
    let temp = showIntents.map((x) => x);
    let newValue = event.target.value;
    let availableIntent = temp.map((image) => image[type]);
    if (availableIntent.includes(newValue) && type === "keyword") {
      notification("error", i18n.t("notify.failExistLabelName"));
    } else {
      temp[indexLabel][type] = event.target.value;
      temp[indexLabel].isModified = true;
      setIntents(temp);
    }
  }

  const onClickChangeBtn = () => {
    dispatch({
      type: "qa/changeIsUploadAction",
    });
  }

  const onClickSaveBtn = () => {
    dispatch({
      type: "qa/createNewIntents",
      payload: {
        intents: showIntents,
      }
    });
  }

  const onClickTrainBtn = () => {
    dispatch({
      type: "qa/trainIntents",
    });
  }

  const onClickApproveBtn = () => {
    dispatch({
      type: "qa/approveNewCheckpoint",
    });
  }

  const onClickCheckStatusBtn = () => {
    dispatch({
      type: "qa/checkStatusTrain",
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
                >Add new question</Button>
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
            {!isUploadAction && (!statusTrain || statusTrain === "approved") && (
              <Button 
                variant="danger" 
                onClick={() => onClickTrainBtn()}
                className="mx-2"
              >Train</Button>
            )}
            {!isUploadAction && statusTrain && statusTrain !== "approved" && (
              <Button 
                variant="success" 
                onClick={() => onClickCheckStatusBtn()}
                className="mx-2"
              >Refresh (status: {statusTrain})</Button>
            )}
            {!isUploadAction && statusTrain === "trained" && (
              <Button 
                variant="danger" 
                onClick={() => onClickApproveBtn()}
                className="mx-2"
              >Approve</Button>
            )}
            {isUploadAction && (
              <Button 
                variant="success" 
                onClick={() => onClickSaveBtn()}
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

      {showIntents.length !== 0 && (
        <Container style={{"maxWidth": "100%"}}>
          {showIntents.map((intent, index) => {
            return (
            <Card className="my-2" style={{ border: "0px" }} key={index}>
              <Form.Group as={Row} className="m-2 p-2" controlId="formUploadName">
                Keyword:
                <Row className="my-2">
                  <Form.Control
                    defaultValue={intent.keyword}
                    onChange={(event) => onChangeLabel(index, "keyword", event)}
                    disabled={!isUploadAction}
                  />
                </Row>
                Questions:
                <Row className="my-2">
                  <Form.Control
                    as="textarea"
                    rows={intent.questions.split(';\n').length}
                    defaultValue={intent.questions}
                    onChange={(event) => onChangeLabel(index, "questions", event)}
                    disabled={!isUploadAction}
                  />
                </Row>
                Answer:
                <Row className="my-2">
                  <Form.Control
                    defaultValue={intent.answer}
                    onChange={(event) => onChangeLabel(index, "answer", event)}
                    disabled={!isUploadAction}
                  />
                </Row>
              </Form.Group>
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

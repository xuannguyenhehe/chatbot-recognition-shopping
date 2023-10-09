import Modal from "@mui/material/Modal";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import "./LayoutDevice.scss";
function LayoutDevice() {
  return (
    <div className="text-center fs-1">
      <Modal open={true}>
        <Box className="modal-box">
          <Typography
            id="modal-modal-title"
            variant="h4"
            component="h2"
            style={{ color: "#080000", fontWeight: "bold" }}
          >
            Sorry!
          </Typography>
          <Typography id="modal-modal-description" sx={{ mt: 2 }}>
            Tessel does not support on your device. Please visit on PC
          </Typography>
        </Box>
      </Modal>
    </div>
  );
}

export default LayoutDevice;

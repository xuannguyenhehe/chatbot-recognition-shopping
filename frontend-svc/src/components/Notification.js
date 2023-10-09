import { toast } from "react-toastify";

/*
    status: 'success', 'warn, 'error'
    content: 'Some text will be show in notification'
    timing (option) => default 5s 
*/
const notification = (status, content = "", timing) => {
  return toast[status](content, {
    position: "top-right",
    autoClose: timing ?? 3000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    progress: undefined,
    theme: "light",
    bodyClassName: "toast-font-size"
  });
};

export default notification;

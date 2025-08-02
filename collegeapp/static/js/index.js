document.addEventListener("DOMContentLoaded", (event) => {
    // Toaster
    function showToast(message, type = "success") {
        const toastContainer = document.querySelector(".toast-container");
      
        const toast = document.createElement("div");
        toast.classList.add("toast", type);
      
        toast.innerHTML = `
          <div class="toast-content">
            <i class="bi icon bi-${getIcon(type)}"></i>
            <div class="message">
              <span class="text text-1">${capitalize(type)}</span>
              <span class="text text-2">${message}</span>
            </div>
          </div>
          <i class="bi bi-x-lg close"></i>
          <div class="progress active"></div>
        `;
      
        toastContainer.appendChild(toast);
        let showToast = setTimeout(() => {
          void toast.offsetHeight;
          toast.classList.add("active");
        }, 1);
      
        const progress = toast.querySelector(".progress");
        const closeIcon = toast.querySelector(".close");
      
        // Auto-remove toast after 5s
        const timer1 = setTimeout(() => {
          toast.classList.remove("active");
        }, 5000);
      
        const timer2 = setTimeout(() => {
          progress.classList.remove("active");
          setTimeout(() => toast.remove(), 400);
        }, 5300);
      
        // Manual close
        closeIcon.addEventListener("click", () => {
          toast.classList.remove("active");
          clearTimeout(timer1);
          clearTimeout(timer2);
          clearTimeout(showToast);
          setTimeout(() => toast.remove(), 400);
        });
      }
      
      function getIcon(type) {
        switch (type) {
          case "success": return "check-circle-fill";
          case "error": return "x-circle-fill";
          case "warning": return "exclamation-triangle-fill";
          case "info": return "info-circle-fill";
          default: return "check-circle-fill";
        }
      }
      
      function capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
      }


    // Validation functions
    const name_validator = (input_name) => {
        return /^[A-Za-z]{3,}(?:\s[A-Za-z]+){0,2}$/.test(input_name.value.trim());
    };
    const subject_validator = (subject_name) => {
        return /^(?=(.*[A-Za-z]){5,})[A-Za-z0-9\s]{1,255}$/.test(subject_name.value.trim());
    };    
    const program_select_validator = (program) => program.value !== "";
    const phone_no_validator = (phone) => {
        const trimmedPhone = phone.value.trim();
        return /^(97|98)\d{7,8}$/.test(trimmedPhone) || /^(01|04|05|06|07)\d{6,7}$/.test(trimmedPhone);
    };
    
    const email_validator = (input_email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input_email.value);
    const pre_college_name_validator = (clz_name) => clz_name.value !== "" && clz_name.value.length >= 3;

    // Apply validation on blur
    const applyBlurValidation = (input, validator, errorElementId, errorMessage) => {
        input.onkeyup = () => {
            const errorElement = document.getElementById(errorElementId);
            if (!validator(input)) {
                input.classList.add("input-error");
                errorElement.textContent = errorMessage;
            } else {
                input.classList.remove("input-error");
                errorElement.textContent = "";
            }
        };
    };

    // Apply validation on submit
    const applySubmitValidation = (form, validations) => {
        form.onsubmit = (event) => {
            let isValid = true;
            validations.forEach(({ input, validator, errorElementId, errorMessage }) => {
                const errorElement = document.getElementById(errorElementId);
                if (!validator(input)) {
                    input.classList.add("input-error");
                    errorElement.textContent = errorMessage;
                    isValid = false;
                } else {
                    input.classList.remove("input-error");
                    errorElement.textContent = "";
                }
            });
            if (!isValid) {
                event.preventDefault();
            }
        };
    };

    // Form elements and their validations
    const forms = [
        {
            form: document.querySelector("form[action='/apply-online']"),
            validations: [
                { input: document.getElementById("fullname"), validator: name_validator, errorElementId: "name-error", errorMessage: "Name can't be less than 3 characters or contain numbers!" },
                // { input: document.getElementById("program"), validator: program_select_validator, errorElementId: "program-error", errorMessage: "At least one program should be selected!" },
                { input: document.getElementById("phone"), validator: phone_no_validator, errorElementId: "phone-error", errorMessage: "Enter a valid phone number!" },
                { input: document.getElementById("email"), validator: email_validator, errorElementId: "email-error", errorMessage: "Please enter a valid email address." },
                { input: document.getElementById("previouscollege"), validator: pre_college_name_validator, errorElementId: "pre-clz-error", errorMessage: "College name must be at least 3 characters long." }
            ]
        },
        {
            form: document.querySelector("form[action='/']"),
            validations: [
                { input: document.getElementById("name"), validator: name_validator, errorElementId: "name-error", errorMessage: "Name can't be less than 3 characters or contain numbers!" },
                { input: document.getElementById("phone"), validator: phone_no_validator, errorElementId: "phone-error", errorMessage: "Enter a valid phone number!" },
                { input: document.getElementById("email"), validator: email_validator, errorElementId: "email-error", errorMessage: "Please enter a valid email address." }
            ]
        },
        {
            form: document.querySelector("form[action='/contact']"),
            validations: [
                { input: document.getElementById("name"), validator: name_validator, errorElementId: "name-error", errorMessage: "Name can't be less than 3 characters or contain numbers!" },
                { input: document.getElementById("phone"), validator: phone_no_validator, errorElementId: "phone-error", errorMessage: "Enter a valid phone number!" },
                { input: document.getElementById("email"), validator: email_validator, errorElementId: "email-error", errorMessage: "Please enter a valid email address." },
                { input: document.getElementById("subject"), validator: subject_validator, errorElementId: "subject-error", errorMessage: "Subject must contain at least 5 letters and can include numbers and spaces!" }
            ]
        }
    ];

    // Apply validations
    forms.forEach(({ form, validations }) => {
        if (form) {
            validations.forEach(({ input, validator, errorElementId, errorMessage }) => {
                if (input) {
                    applyBlurValidation(input, validator, errorElementId, errorMessage);
                }
            });
            applySubmitValidation(form, validations);
        }
    });

    // Footer email validation
    const footerEmailInput = document.getElementById("footer-email");
    const footerEmailError = document.getElementById("footer-email-error");
    const subscribeBtn = document.getElementById("subscribe-btn");

    subscribeBtn.onclick = (event) => {
        if (!email_validator(footerEmailInput)) {
            footerEmailInput.classList.add("input-error");
            footerEmailError.textContent = "Please enter a valid email address.";
            event.preventDefault();
        } else {
            footerEmailInput.classList.remove("input-error");
            footerEmailError.textContent = "";
        }
    };

    footerEmailInput.onkeyup = () => {
        if (!email_validator(footerEmailInput)) {
            footerEmailInput.classList.add("input-error");
            footerEmailError.textContent = "Please enter a valid email address.";
        } else {
            footerEmailInput.classList.remove("input-error");
            footerEmailError.textContent = "";
        }
    };
});

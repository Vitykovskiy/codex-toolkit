export function textField(name, label, type = "text") {
  const wrapper = document.createElement("label");
  wrapper.textContent = label;
  const input = document.createElement("input");
  Object.assign(input, { name, type, required: true });
  wrapper.append(input);
  return wrapper;
}

export function submitButton() {
  const button = document.createElement("button");
  button.type = "submit";
  button.textContent = "Send";
  return button;
}

export function messageRegion(kind) {
  const region = document.createElement("p");
  region.id = kind;
  region.tabIndex = -1;
  region.setAttribute("role", kind === "error" ? "alert" : "status");
  return region;
}

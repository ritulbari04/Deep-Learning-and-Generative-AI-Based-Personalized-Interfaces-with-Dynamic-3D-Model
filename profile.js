document.addEventListener("DOMContentLoaded", function () {
  const editButton = document.getElementById("edit-profile");
  const profileCard = document.querySelector(".profile-card");

  let isEditing = false;

  editButton.addEventListener("click", function () {
    if (!isEditing) {
      // Enter edit mode
      const name = profileCard.querySelector("h2").innerText;
      const email = profileCard.querySelector(".email").innerText;

      profileCard.innerHTML = `
        <div class="avatar"></div>
        <input type="text" id="edit-name" value="${name}" class="edit-input" />
        <input type="email" id="edit-email" value="${email}" class="edit-input" />
        <button id="save-profile" class="edit-btn">Save</button>
        <button id="cancel-edit" class="edit-btn">Cancel</button>
      `;

      isEditing = true;

      document.getElementById("save-profile").addEventListener("click", function () {
        const newName = document.getElementById("edit-name").value.trim();
        const newEmail = document.getElementById("edit-email").value.trim();

        if (newName === "" || newEmail === "") {
          alert("Name and email cannot be empty.");
          return;
        }

        profileCard.innerHTML = `
          <div class="avatar"></div>
          <h2>${newName}</h2>
          <p class="email">${newEmail}</p>
          <button class="edit-btn" id="edit-profile">Edit Profile</button>
        `;

        isEditing = false;

        // Reattach event listener
        document.getElementById("edit-profile").addEventListener("click", arguments.callee);
      });

      document.getElementById("cancel-edit").addEventListener("click", function () {
        profileCard.innerHTML = `
          <div class="avatar"></div>
          <h2>${name}</h2>
          <p class="email">${email}</p>
          <button class="edit-btn" id="edit-profile">Edit Profile</button>
        `;

        isEditing = false;

        // Reattach event listener
        document.getElementById("edit-profile").addEventListener("click", arguments.callee);
      });
    }
  });
});

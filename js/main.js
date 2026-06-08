(function () {
  "use strict";

  const config = window.CDP || {};
  const dateTbd = Boolean(config.PARTY_DATE_TBD || !config.PARTY_DATE);
  const PARTY_DATE = config.PARTY_DATE ? new Date(config.PARTY_DATE) : null;
  const PARTY_END = config.PARTY_END ? new Date(config.PARTY_END) : null;

  const daysEl = document.getElementById("days");
  const hoursEl = document.getElementById("hours");
  const minutesEl = document.getElementById("minutes");
  const secondsEl = document.getElementById("seconds");
  const countdownEl = document.querySelector(".countdown");
  const dateTbdEl = document.getElementById("date-tbd");
  const postPartyEl = document.getElementById("post-party");
  const heroEyebrow = document.getElementById("hero-eyebrow");
  const heroTagline = document.getElementById("hero-tagline");
  const partyNightEl = document.getElementById("party-night");

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function applyDateTbdMode() {
    if (!dateTbd) {
      return;
    }

    document.body.classList.add("is-date-tbd");

    if (countdownEl) {
      countdownEl.classList.add("is-hidden");
    }

    if (dateTbdEl) {
      dateTbdEl.classList.remove("is-hidden");
    }
  }

  function isPostParty() {
    if (dateTbd || !PARTY_END) {
      return false;
    }
    return Date.now() >= PARTY_END.getTime();
  }

  function isPartyLive() {
    if (dateTbd || !PARTY_DATE || !PARTY_END) {
      return false;
    }
    const now = Date.now();
    return now >= PARTY_DATE.getTime() && now < PARTY_END.getTime();
  }

  function applyPostPartyMode() {
    if (!isPostParty()) {
      return;
    }

    document.body.classList.add("is-post-party");

    if (heroEyebrow) {
      heroEyebrow.innerHTML =
        '<span class="star" aria-hidden="true">★</span> Thanks for Dancing <span class="star" aria-hidden="true">★</span>';
    }

    if (heroTagline) {
      heroTagline.textContent = "Relive the two-step, share photos, and help us plan the next one.";
    }

    if (countdownEl) {
      countdownEl.classList.add("is-hidden");
    }

    if (dateTbdEl) {
      dateTbdEl.classList.add("is-hidden");
    }

    if (postPartyEl) {
      postPartyEl.classList.remove("is-hidden");
    }

    if (partyNightEl) {
      partyNightEl.querySelector(".party-night__heading").textContent = "Keep the Party Going";
      partyNightEl.querySelector(".party-night__lead").textContent =
        "Upload photos, vote for best outfit, and tell us when to do it all again.";
    }
  }

  function applyLivePartyMode() {
    if (!isPartyLive()) {
      return;
    }

    document.body.classList.add("is-party-live");

    if (heroEyebrow) {
      heroEyebrow.innerHTML =
        '<span class="star" aria-hidden="true">★</span> Party Night <span class="star" aria-hidden="true">★</span>';
    }

    if (heroTagline) {
      heroTagline.textContent =
        "Boots. Bling. Mirror ball till dawn — scan the QR for photos, ice breakers, and votes.";
    }

    if (countdownEl) {
      countdownEl.classList.add("is-hidden");
    }

    if (dateTbdEl) {
      dateTbdEl.classList.add("is-hidden");
    }

    if (postPartyEl) {
      postPartyEl.classList.add("is-hidden");
    }
  }

  function updateCountdown() {
    applyDateTbdMode();

    if (dateTbd) {
      return;
    }

    if (!daysEl || !hoursEl || !minutesEl || !secondsEl || !PARTY_DATE) {
      applyPostPartyMode();
      applyLivePartyMode();
      return;
    }

    if (isPostParty()) {
      applyPostPartyMode();
      return;
    }

    if (isPartyLive()) {
      applyLivePartyMode();
      return;
    }

    const diff = PARTY_DATE.getTime() - Date.now();
    if (diff <= 0) {
      daysEl.textContent = "00";
      hoursEl.textContent = "00";
      minutesEl.textContent = "00";
      secondsEl.textContent = "00";
      applyLivePartyMode();
      return;
    }

    const totalSeconds = Math.floor(diff / 1000);
    const days = Math.floor(totalSeconds / 86400);
    const hours = Math.floor((totalSeconds % 86400) / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;

    daysEl.textContent = pad(days);
    hoursEl.textContent = pad(hours);
    minutesEl.textContent = pad(minutes);
    secondsEl.textContent = pad(seconds);
  }

  updateCountdown();
  setInterval(updateCountdown, 1000);
  applyPostPartyMode();
  applyLivePartyMode();

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").catch(function () {
        /* offline support is optional */
      });
    });
  }
})();

import React, { useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  Activity,
  Camera,
  ClipboardCheck,
  ClipboardList,
  FileImage,
  LogIn,
  LogOut,
  Loader2,
  LockKeyhole,
  RefreshCw,
  ShieldAlert,
  Stethoscope,
  Upload,
  UserPlus,
  UserRound,
  Volume2,
  VolumeX,
} from "lucide-react";
import "./styles.css";

const API_BASE_URL = "http://127.0.0.1:8000";

const initialForm = {
  patient_name: "",
  age: "",
  gender: "Male",
  body_location: "",
  itch: "yes",
  pain: "no",
  symptoms: "",
  image: null,
};

const initialAuthForm = {
  full_name: "",
  email: "",
  password: "",
  role: "patient",
};

function confidencePercent(confidence) {
  const value = Number(confidence || 0);
  return value <= 1 ? value * 100 : value;
}

function modelStatusText(status) {
  if (status === "real") {
    return "Real AI model";
  }
  if (status === "dummy") {
    return "Demo prediction";
  }
  return "Model status unavailable";
}

function App() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const cameraStreamRef = useRef(null);
  const savedSession = useMemo(() => {
    const rawSession = localStorage.getItem("eiot_session");
    return rawSession ? JSON.parse(rawSession) : null;
  }, []);

  const [session, setSession] = useState(savedSession);
  const [authMode, setAuthMode] = useState("login");
  const [authForm, setAuthForm] = useState(initialAuthForm);
  const [authError, setAuthError] = useState("");
  const [isAuthLoading, setIsAuthLoading] = useState(false);
  const [activeView, setActiveView] = useState(
    savedSession?.user.role === "doctor" ? "doctor" : "patient",
  );
  const [form, setForm] = useState(initialForm);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [cases, setCases] = useState([]);
  const [casesError, setCasesError] = useState("");
  const [isLoadingCases, setIsLoadingCases] = useState(false);
  const [reviewDrafts, setReviewDrafts] = useState({});
  const [updatingCaseId, setUpdatingCaseId] = useState(null);
  const [cameraStream, setCameraStream] = useState(null);
  const [cameraError, setCameraError] = useState("");
  const [isCameraOpen, setIsCameraOpen] = useState(false);

  const imagePreview = useMemo(() => {
    if (!form.image) {
      return null;
    }
    return URL.createObjectURL(form.image);
  }, [form.image]);

  useEffect(() => {
    if (videoRef.current && cameraStream) {
      videoRef.current.srcObject = cameraStream;
    }
  }, [cameraStream]);

  useEffect(() => {
    return () => {
      stopCamera(false);
    };
  }, []);

  function updateField(name, value) {
    setForm((current) => ({ ...current, [name]: value }));
  }

  function updateAuthField(name, value) {
    setAuthForm((current) => ({ ...current, [name]: value }));
  }

  function authHeaders(tokenOverride) {
    return {
      Authorization: `Bearer ${tokenOverride || session?.token}`,
    };
  }

  async function startCamera() {
    setCameraError("");

    if (!navigator.mediaDevices?.getUserMedia) {
      setCameraError("Camera is not supported in this browser.");
      return;
    }

    try {
      if (cameraStreamRef.current) {
        stopCamera();
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "environment",
        },
        audio: false,
      });
      cameraStreamRef.current = stream;
      setCameraStream(stream);
      setIsCameraOpen(true);
    } catch (requestError) {
      setCameraError(
        requestError.message ||
          "Unable to access camera. Please allow camera permission in the browser.",
      );
    }
  }

  function stopCamera(updateState = true) {
    if (cameraStreamRef.current) {
      cameraStreamRef.current.getTracks().forEach((track) => track.stop());
      cameraStreamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    if (updateState) {
      setCameraStream(null);
      setIsCameraOpen(false);
    }
  }

  function capturePhoto() {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas) {
      setCameraError("Camera preview is not ready yet.");
      return;
    }

    const width = video.videoWidth || 1280;
    const height = video.videoHeight || 720;
    canvas.width = width;
    canvas.height = height;

    const context = canvas.getContext("2d");
    context.drawImage(video, 0, 0, width, height);

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setCameraError("Unable to capture image. Please try again.");
          return;
        }

        const capturedFile = new File([blob], `camera-capture-${Date.now()}.jpg`, {
          type: "image/jpeg",
        });
        updateField("image", capturedFile);
        setCameraError("");
        stopCamera();
      },
      "image/jpeg",
      0.92,
    );
  }

  function handleImageUpload(file) {
    if (!file) {
      return;
    }
    stopCamera();
    setCameraError("");
    updateField("image", file);
  }

  async function submitAuth(event) {
    event.preventDefault();
    setAuthError("");
    setIsAuthLoading(true);

    const endpoint = authMode === "login" ? "/auth/login" : "/auth/register";
    const payload =
      authMode === "login"
        ? { email: authForm.email, password: authForm.password }
        : authForm;

    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Authentication failed.");
      }

      const data = await response.json();
      localStorage.setItem("eiot_session", JSON.stringify(data));
      setSession(data);
      setForm((current) => ({
        ...current,
        patient_name: data.user.role === "patient" ? data.user.full_name : current.patient_name,
      }));
      setActiveView(data.user.role === "doctor" ? "doctor" : "patient");

      if (data.user.role === "doctor") {
        loadCases(data.token);
      }
    } catch (requestError) {
      setAuthError(requestError.message || "Unable to login.");
    } finally {
      setIsAuthLoading(false);
    }
  }

  async function logout() {
    if (session?.token) {
      await fetch(`${API_BASE_URL}/auth/logout`, {
        method: "POST",
        headers: authHeaders(),
      }).catch(() => {});
    }

    localStorage.removeItem("eiot_session");
    setSession(null);
    setResult(null);
    setCases([]);
    setActiveView("patient");
  }

  async function submitCase(event) {
    event.preventDefault();
    setError("");
    setResult(null);

    if (!form.image) {
      setError("Please upload a skin image before submitting.");
      return;
    }

    const payload = new FormData();
    Object.entries(form).forEach(([key, value]) => {
      payload.append(key, value);
    });

    setIsSubmitting(true);

    try {
      const response = await fetch(`${API_BASE_URL}/predict`, {
        method: "POST",
        headers: authHeaders(),
        body: payload,
      });

      if (!response.ok) {
        throw new Error("Backend rejected the request. Please check all fields.");
      }

      const data = await response.json();
      setResult(data);
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to connect to backend. Make sure FastAPI is running on port 8000.",
      );
    } finally {
      setIsSubmitting(false);
    }
  }

  async function loadCases(tokenOverride) {
    setCasesError("");
    setIsLoadingCases(true);

    try {
      const response = await fetch(`${API_BASE_URL}/cases`, {
        headers: authHeaders(tokenOverride),
      });

      if (!response.ok) {
        throw new Error("Unable to load cases from backend.");
      }

      const data = await response.json();
      setCases(data);
    } catch (requestError) {
      setCasesError(
        requestError.message ||
          "Could not connect to backend. Make sure FastAPI is running.",
      );
    } finally {
      setIsLoadingCases(false);
    }
  }

  function openDoctorView() {
    setActiveView("doctor");
    loadCases();
  }

  function updateReviewDraft(caseId, field, value) {
    setReviewDrafts((current) => ({
      ...current,
      [caseId]: {
        doctor_status: current[caseId]?.doctor_status || "Reviewed",
        doctor_notes: current[caseId]?.doctor_notes || "",
        [field]: value,
      },
    }));
  }

  async function submitReview(caseId) {
    const draft = reviewDrafts[caseId] || {
      doctor_status: "Reviewed",
      doctor_notes: "",
    };

    setUpdatingCaseId(caseId);
    setCasesError("");

    try {
      const response = await fetch(`${API_BASE_URL}/cases/${caseId}/review`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          ...authHeaders(),
        },
        body: JSON.stringify(draft),
      });

      if (!response.ok) {
        throw new Error("Unable to update doctor review.");
      }

      const updatedCase = await response.json();
      setCases((current) =>
        current.map((caseItem) => (caseItem.id === caseId ? updatedCase : caseItem)),
      );
    } catch (requestError) {
      setCasesError(requestError.message || "Review update failed.");
    } finally {
      setUpdatingCaseId(null);
    }
  }

  function speakReport() {
    if (!result || !("speechSynthesis" in window)) {
      return;
    }

    window.speechSynthesis.cancel();

    const reportText =
      result.voice_text ||
      [
        `Screening report for ${result.patient_name}.`,
        `Possible condition is ${result.disease || result.predicted_disease}.`,
        `Confidence is ${confidencePercent(result.confidence).toFixed(1)} percent.`,
        `Risk level is ${result.risk_level}.`,
        result.recommendation,
        `Doctor review status is ${result.doctor_status}.`,
      ].join(" ");

    const utterance = new SpeechSynthesisUtterance(reportText);
    utterance.rate = 0.92;
    utterance.pitch = 1;
    window.speechSynthesis.speak(utterance);
  }

  function stopVoiceReport() {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
  }

  return (
    <main className="app-shell">
      <section className="intro-panel">
        <div>
          <p className="eyebrow">Embedded Systems and IoT</p>
          <h1>Smart Remote Skin Disease Screening</h1>
          <p className="intro-copy">
            Patient image and symptom data are sent to the backend, where the AI
            prediction module will be connected after training.
          </p>
        </div>
        <div className="status-strip" aria-label="Project status">
          <span>
            <Camera size={18} />
            Camera Input
          </span>
          <span>
            <Activity size={18} />
            AI Screening
          </span>
          <span>
            <Stethoscope size={18} />
            Doctor Review
          </span>
        </div>
      </section>

      {!session ? (
        <section className="auth-layout">
          <form className="auth-card" onSubmit={submitAuth}>
            <div className="section-title">
              <LockKeyhole size={22} />
              <h2>{authMode === "login" ? "Login" : "Create Account"}</h2>
            </div>

            {authMode === "register" && (
              <>
                <label>
                  Full Name
                  <input
                    required
                    type="text"
                    value={authForm.full_name}
                    onChange={(event) => updateAuthField("full_name", event.target.value)}
                    placeholder="Enter full name"
                  />
                </label>

                <label>
                  Account Type
                  <select
                    value={authForm.role}
                    onChange={(event) => updateAuthField("role", event.target.value)}
                  >
                    <option value="patient">Patient</option>
                    <option value="doctor">Doctor</option>
                  </select>
                </label>
              </>
            )}

            <label>
              Email
              <input
                required
                type="email"
                value={authForm.email}
                onChange={(event) => updateAuthField("email", event.target.value)}
                placeholder="name@example.com"
              />
            </label>

            <label>
              Password
              <input
                required
                minLength="6"
                type="password"
                value={authForm.password}
                onChange={(event) => updateAuthField("password", event.target.value)}
                placeholder="Minimum 6 characters"
              />
            </label>

            {authError && <p className="error-message">{authError}</p>}

            <button className="submit-button" type="submit" disabled={isAuthLoading}>
              {isAuthLoading ? (
                <Loader2 className="spin" size={20} />
              ) : authMode === "login" ? (
                <LogIn size={20} />
              ) : (
                <UserPlus size={20} />
              )}
              {authMode === "login" ? "Login" : "Create Account"}
            </button>

            <button
              className="link-button"
              type="button"
              onClick={() => {
                setAuthError("");
                setAuthMode(authMode === "login" ? "register" : "login");
              }}
            >
              {authMode === "login"
                ? "Need an account? Sign up"
                : "Already have an account? Login"}
            </button>
          </form>

          <div className="auth-info">
            <h2>Role Based Access</h2>
            <p>
              Patients can submit screening cases. Doctors can view submitted
              cases and save validation notes.
            </p>
            <div className="auth-info-grid">
              <span>Patient privacy</span>
              <span>Doctor review</span>
              <span>Token login</span>
              <span>Password hashing</span>
            </div>
          </div>
        </section>
      ) : (
      <>
      <div className="account-strip">
        <span>
          Logged in as <strong>{session.user.full_name}</strong> ({session.user.role})
        </span>
        <button className="secondary-button" type="button" onClick={logout}>
          <LogOut size={18} />
          Logout
        </button>
      </div>

      <nav className="view-switcher" aria-label="Application views">
        {session.user.role === "patient" && (
        <button
          className={activeView === "patient" ? "active" : ""}
          type="button"
          onClick={() => setActiveView("patient")}
        >
          <UserRound size={18} />
          Patient App
        </button>
        )}
        {session.user.role === "doctor" && (
        <button
          className={activeView === "doctor" ? "active" : ""}
          type="button"
          onClick={openDoctorView}
        >
          <Stethoscope size={18} />
          Doctor Dashboard
        </button>
        )}
      </nav>

      {activeView === "patient" && session.user.role === "patient" ? (
      <section className="workspace-grid">
        <form className="patient-form" onSubmit={submitCase}>
          <div className="section-title">
            <UserRound size={22} />
            <h2>Patient Details</h2>
          </div>

          <label>
            Patient Name
            <input
              required
              type="text"
              value={form.patient_name}
              onChange={(event) => updateField("patient_name", event.target.value)}
              placeholder="Enter patient name"
            />
          </label>

          <div className="field-row">
            <label>
              Age
              <input
                required
                min="1"
                max="120"
                type="number"
                value={form.age}
                onChange={(event) => updateField("age", event.target.value)}
                placeholder="21"
              />
            </label>

            <label>
              Gender
              <select
                value={form.gender}
                onChange={(event) => updateField("gender", event.target.value)}
              >
                <option>Male</option>
                <option>Female</option>
                <option>Other</option>
              </select>
            </label>
          </div>

          <label>
            Affected Body Location
            <input
              required
              type="text"
              value={form.body_location}
              onChange={(event) => updateField("body_location", event.target.value)}
              placeholder="Arm, face, neck, leg..."
            />
          </label>

          <div className="field-row">
            <label>
              Itching
              <select
                value={form.itch}
                onChange={(event) => updateField("itch", event.target.value)}
              >
                <option value="yes">Yes</option>
                <option value="no">No</option>
              </select>
            </label>

            <label>
              Pain
              <select
                value={form.pain}
                onChange={(event) => updateField("pain", event.target.value)}
              >
                <option value="no">No</option>
                <option value="yes">Yes</option>
              </select>
            </label>
          </div>

          <label>
            Symptoms
            <textarea
              value={form.symptoms}
              onChange={(event) => updateField("symptoms", event.target.value)}
              placeholder="Describe redness, swelling, circular patches, spreading, fever, etc."
            />
          </label>

          <label className="upload-box">
            <input
              type="file"
              accept="image/png,image/jpeg"
              onChange={(event) => handleImageUpload(event.target.files[0])}
            />
            <span>
              <Upload size={20} />
              Upload Skin Image
            </span>
            <small>{form.image ? form.image.name : "JPG or PNG image"}</small>
          </label>

          <div className="camera-panel">
            <div className="camera-panel-header">
              <Camera size={20} />
              <strong>Laptop Camera</strong>
            </div>

            {isCameraOpen ? (
              <>
                <video
                  ref={videoRef}
                  className="camera-preview"
                  autoPlay
                  muted
                  playsInline
                />
                <div className="camera-actions">
                  <button className="camera-button primary" type="button" onClick={capturePhoto}>
                    <Camera size={18} />
                    Capture Photo
                  </button>
                  <button className="camera-button" type="button" onClick={stopCamera}>
                    <VolumeX size={18} />
                    Stop Camera
                  </button>
                </div>
              </>
            ) : (
              <button className="camera-button primary" type="button" onClick={startCamera}>
                <Camera size={18} />
                Start Camera
              </button>
            )}

            {form.image && (
              <button className="camera-button" type="button" onClick={startCamera}>
                <RefreshCw size={18} />
                Retake With Camera
              </button>
            )}

            {cameraError && <p className="error-message">{cameraError}</p>}
            <canvas ref={canvasRef} className="hidden-canvas" />
          </div>

          {error && <p className="error-message">{error}</p>}

          <button className="submit-button" type="submit" disabled={isSubmitting}>
            {isSubmitting ? <Loader2 className="spin" size={20} /> : <ClipboardCheck size={20} />}
            {isSubmitting ? "Submitting Case" : "Submit For Screening"}
          </button>
        </form>

        <aside className="result-panel">
          <div className="section-title">
            <ShieldAlert size={22} />
            <h2>Screening Result</h2>
          </div>

          {imagePreview ? (
            <img className="preview-image" src={imagePreview} alt="Selected skin area" />
          ) : (
            <div className="empty-preview">
              <FileImage size={42} />
              <span>Image preview will appear here</span>
            </div>
          )}

          {result ? (
            <div className="result-card">
              <span className={`risk-pill risk-${result.risk_level.toLowerCase().replaceAll(" ", "-")}`}>
                {result.risk_level}
              </span>
              <h3>{result.disease || result.predicted_disease}</h3>
              <p className="confidence">{confidencePercent(result.confidence).toFixed(1)}% confidence</p>
              <span className={`model-status model-${result.model_status || "unknown"}`}>
                {modelStatusText(result.model_status)}
              </span>
              <p>{result.recommendation}</p>
              {result.doctor_reason && (
                <p className="doctor-reason">{result.doctor_reason}</p>
              )}
              {result.medicine_guidance && (
                <div className="medicine-panel">
                  <h4>Medicine Guidance</h4>
                  <p><strong>Category:</strong> {result.medicine_guidance.category}</p>
                  <p><strong>Examples:</strong> {result.medicine_guidance.examples.join(", ")}</p>
                  <p>{result.medicine_guidance.instruction}</p>
                  <small>Final medicine or prescription should be verified by a doctor.</small>
                </div>
              )}
              {result.top_3_predictions?.length > 0 && (
                <div className="top-predictions">
                  <h4>Top 3 Predictions</h4>
                  {result.top_3_predictions.map((item) => (
                    <div className="prediction-row" key={item.disease}>
                      <span>{item.disease}</span>
                      <strong>{confidencePercent(item.confidence).toFixed(1)}%</strong>
                    </div>
                  ))}
                </div>
              )}
              <dl>
                <div>
                  <dt>Case ID</dt>
                  <dd>{result.id}</dd>
                </div>
                <div>
                  <dt>Doctor Status</dt>
                  <dd>{result.doctor_status}</dd>
                </div>
              </dl>
              <div className="voice-actions">
                <button className="voice-button" type="button" onClick={speakReport}>
                  <Volume2 size={18} />
                  Play Voice Report
                </button>
                <button className="voice-button quiet" type="button" onClick={stopVoiceReport}>
                  <VolumeX size={18} />
                  Stop
                </button>
              </div>
            </div>
          ) : (
            <p className="muted">
              Submit a patient case to see the backend response.
            </p>
          )}
        </aside>
      </section>
      ) : (
        <section className="doctor-dashboard">
          <div className="dashboard-header">
            <div className="section-title">
              <ClipboardList size={22} />
              <h2>Doctor Dashboard</h2>
            </div>
            <button className="secondary-button" type="button" onClick={loadCases}>
              {isLoadingCases ? <Loader2 className="spin" size={18} /> : <RefreshCw size={18} />}
              Refresh Cases
            </button>
          </div>

          {casesError && <p className="error-message">{casesError}</p>}

          {cases.length === 0 && !isLoadingCases ? (
            <div className="empty-state">
              <Stethoscope size={44} />
              <h3>No cases yet</h3>
              <p>Submit a patient case first, then refresh this dashboard.</p>
            </div>
          ) : (
            <div className="case-list">
              {cases.map((caseItem) => {
                const draft = reviewDrafts[caseItem.id] || {
                  doctor_status: caseItem.doctor_status,
                  doctor_notes: caseItem.doctor_notes || "",
                };

                return (
                  <article className="case-card" key={caseItem.id}>
                    <img
                      className="case-image"
                      src={`${API_BASE_URL}${caseItem.image_path}`}
                      alt={`Case ${caseItem.id}`}
                    />

                    <div className="case-content">
                      <div className="case-topline">
                        <span className={`risk-pill risk-${caseItem.risk_level.toLowerCase().replaceAll(" ", "-")}`}>
                          {caseItem.risk_level}
                        </span>
                        <span className="case-date">{caseItem.created_at}</span>
                      </div>

                      <h3>{caseItem.disease || caseItem.predicted_disease}</h3>
                      <p className="confidence">{confidencePercent(caseItem.confidence).toFixed(1)}% confidence</p>
                      <span className={`model-status model-${caseItem.model_status || "unknown"}`}>
                        {modelStatusText(caseItem.model_status)}
                      </span>

                      <div className="case-grid">
                        <div>
                          <strong>Patient</strong>
                          <span>{caseItem.patient_name}, {caseItem.age}, {caseItem.gender}</span>
                        </div>
                        <div>
                          <strong>Location</strong>
                          <span>{caseItem.body_location}</span>
                        </div>
                        <div>
                          <strong>Itching</strong>
                          <span>{caseItem.itch}</span>
                        </div>
                        <div>
                          <strong>Pain</strong>
                          <span>{caseItem.pain}</span>
                        </div>
                      </div>

                      <p className="symptom-text">
                        <strong>Symptoms:</strong> {caseItem.symptoms || "No extra symptoms entered"}
                      </p>

                      <p className="recommendation-text">{caseItem.recommendation}</p>
                      {caseItem.medicine_guidance && (
                        <div className="medicine-panel compact">
                          <h4>Medicine Guidance</h4>
                          <p><strong>Category:</strong> {caseItem.medicine_guidance.category}</p>
                          <p><strong>Examples:</strong> {caseItem.medicine_guidance.examples.join(", ")}</p>
                          <p>{caseItem.medicine_guidance.instruction}</p>
                        </div>
                      )}
                      {caseItem.top_3_predictions?.length > 0 && (
                        <div className="top-predictions compact">
                          <h4>Top 3 Predictions</h4>
                          {caseItem.top_3_predictions.map((item) => (
                            <div className="prediction-row" key={item.disease}>
                              <span>{item.disease}</span>
                              <strong>{confidencePercent(item.confidence).toFixed(1)}%</strong>
                            </div>
                          ))}
                        </div>
                      )}

                      <div className="review-box">
                        <label>
                          Review Status
                          <select
                            value={draft.doctor_status}
                            onChange={(event) =>
                              updateReviewDraft(caseItem.id, "doctor_status", event.target.value)
                            }
                          >
                            <option>Pending</option>
                            <option>Reviewed</option>
                            <option>Needs Consultation</option>
                            <option>Urgent Follow-up</option>
                          </select>
                        </label>

                        <label>
                          Doctor Notes
                          <textarea
                            value={draft.doctor_notes}
                            onChange={(event) =>
                              updateReviewDraft(caseItem.id, "doctor_notes", event.target.value)
                            }
                            placeholder="Add validation notes or next action"
                          />
                        </label>

                        <button
                          className="submit-button"
                          type="button"
                          onClick={() => submitReview(caseItem.id)}
                          disabled={updatingCaseId === caseItem.id}
                        >
                          {updatingCaseId === caseItem.id ? (
                            <Loader2 className="spin" size={20} />
                          ) : (
                            <ClipboardCheck size={20} />
                          )}
                          Save Doctor Review
                        </button>
                      </div>
                    </div>
                  </article>
                );
              })}
            </div>
          )}
        </section>
      )}
      </>
      )}
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);

import {
  BookOpen,
  Gauge,
  Glasses,
  HeartPulse,
  History,
  ImagePlus,
  LogOut,
  Palette,
  RefreshCw,
  Scissors,
  ShieldCheck,
  Shirt,
  Sparkles,
  Upload,
  User,
} from "lucide-react";
import React, { useEffect, useMemo, useState } from "react";
import { apiRequest, clearToken, getToken, setToken } from "./services/api.js";

const blueprintCards = [
  {
    title: "Core Build",
    text: "Registration, JWT-style sessions, profile preferences, photo upload, recommendation history, and admin analytics.",
  },
  {
    title: "AI Workflow",
    text: "Image upload, face detection placeholder, feature analysis, face-shape classification, and recommendation output.",
  },
  {
    title: "Recommendation Areas",
    text: "Hairstyles, beard balance, outfits, accessories, glasses, colors, grooming, and wellness routines.",
  },
  {
    title: "Project Roadmap",
    text: "Replace the deterministic MVP analyzer with OpenCV, MediaPipe, and trained ML models when the dataset is ready.",
  },
];

const defaultPreferences = {
  favorite_style: "Smart casual",
  profession: "Student",
  occasion: "Everyday",
  wellness_focus: "Energy",
};

function formatDate(value) {
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  }).format(new Date(value));
}

function AuthScreen({ onAuth }) {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ name: "", email: "demo@example.com", password: "demo123" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const path = mode === "login" ? "/auth/login" : "/auth/register";
      const payload =
        mode === "login"
          ? { email: form.email, password: form.password }
          : { name: form.name, email: form.email, password: form.password };
      const data = await apiRequest(path, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setToken(data.token);
      onAuth(data.user);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function fillAdmin() {
    setMode("login");
    setForm({ name: "", email: "admin@example.com", password: "admin123" });
  }

  return (
    <main className="auth-screen">
      <section className="auth-panel" aria-label="Authentication">
        <div className="brand-row">
          <span className="brand-mark">
            <Sparkles size={21} />
          </span>
          <div>
            <p className="eyebrow">AI Personal Style & Wellness Advisor</p>
            <h1>Style analysis workspace</h1>
          </div>
        </div>

        <div className="mode-switch" role="tablist" aria-label="Authentication mode">
          <button className={mode === "login" ? "active" : ""} onClick={() => setMode("login")} type="button">
            Login
          </button>
          <button className={mode === "register" ? "active" : ""} onClick={() => setMode("register")} type="button">
            Register
          </button>
        </div>

        <form onSubmit={submit} className="auth-form">
          {mode === "register" && (
            <label>
              Name
              <input
                value={form.name}
                onChange={(event) => setForm({ ...form, name: event.target.value })}
                placeholder="Your name"
              />
            </label>
          )}
          <label>
            Email
            <input
              type="email"
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              placeholder="demo@example.com"
            />
          </label>
          <label>
            Password
            <input
              type="password"
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              placeholder="demo123"
            />
          </label>

          {error && <p className="error-text">{error}</p>}

          <button className="primary-action" disabled={loading} type="submit">
            {loading ? <RefreshCw className="spin" size={18} /> : <User size={18} />}
            {mode === "login" ? "Enter dashboard" : "Create account"}
          </button>
        </form>

        <div className="demo-row">
          <button type="button" onClick={() => setForm({ name: "", email: "demo@example.com", password: "demo123" })}>
            Demo user
          </button>
          <button type="button" onClick={fillAdmin}>
            Admin
          </button>
        </div>
      </section>

      <section className="project-brief" aria-label="Project blueprint">
        <div className="brief-header">
          <p className="eyebrow">From the PDF master guide</p>
          <h2>Full-stack MVP, ready to run locally</h2>
        </div>
        <div className="brief-preview" aria-hidden="true">
          <div className="face-card">
            <span className="face-shape" />
            <strong>Oval</strong>
          </div>
          <div className="preview-metrics">
            <span style={{ width: "86%" }} />
            <span style={{ width: "72%" }} />
            <span style={{ width: "64%" }} />
          </div>
          <div className="preview-swatches">
            <span style={{ backgroundColor: "#1f6f68" }} />
            <span style={{ backgroundColor: "#f2b880" }} />
            <span style={{ backgroundColor: "#d95d39" }} />
            <span style={{ backgroundColor: "#f7f3e8" }} />
          </div>
        </div>
        <div className="brief-grid">
          {blueprintCards.map((card) => (
            <article key={card.title}>
              <h3>{card.title}</h3>
              <p>{card.text}</p>
            </article>
          ))}
        </div>
      </section>
    </main>
  );
}

function Sidebar({ view, setView, user }) {
  const items = [
    ["advisor", "Advisor", Sparkles],
    ["history", "History", History],
    ["profile", "Profile", User],
    ["feedback", "Feedback", HeartPulse],
    ["guide", "Guide", BookOpen],
  ];

  if (user.role === "admin") {
    items.push(["admin", "Admin", ShieldCheck]);
  }

  return (
    <aside className="sidebar">
      <div className="sidebar-title">
        <span className="brand-mark small">
          <Sparkles size={18} />
        </span>
        <span>Advisor</span>
      </div>
      <nav>
        {items.map(([key, label, Icon]) => (
          <button key={key} className={view === key ? "active" : ""} onClick={() => setView(key)} type="button">
            <Icon size={18} />
            {label}
          </button>
        ))}
      </nav>
    </aside>
  );
}

function Topbar({ user, onLogout }) {
  return (
    <header className="topbar">
      <div>
        <p className="eyebrow">Dashboard</p>
        <h1>AI Style & Wellness Advisor</h1>
      </div>
      <div className="user-chip">
        <span>
          <User size={16} />
          {user.name}
        </span>
        <button onClick={onLogout} type="button" aria-label="Logout">
          <LogOut size={18} />
        </button>
      </div>
    </header>
  );
}

function AdvisorView({ user, onUserUpdate, onHistoryUpdate, history, selectedResult }) {
  const [form, setForm] = useState({
    favorite_style: user.favorite_style || defaultPreferences.favorite_style,
    profession: user.profession || defaultPreferences.profession,
    occasion: user.occasion_preference || defaultPreferences.occasion,
    wellness_focus: user.wellness_focus || defaultPreferences.wellness_focus,
  });
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const stats = useMemo(
    () => [
      { label: "Saved analyses", value: history.length },
      { label: "Preferred style", value: form.favorite_style },
      { label: "Wellness focus", value: form.wellness_focus },
    ],
    [form.favorite_style, form.wellness_focus, history.length],
  );

  useEffect(() => {
    if (selectedResult) {
      setResult(selectedResult);
    }
  }, [selectedResult]);

  function chooseFile(event) {
    const upload = event.target.files?.[0];
    setFile(upload || null);
    setMessage("");
    if (preview) {
      URL.revokeObjectURL(preview);
    }
    setPreview(upload ? URL.createObjectURL(upload) : "");
  }

  async function submitAnalysis(event) {
    event.preventDefault();
    if (!file) {
      setMessage("Choose a face photo first.");
      return;
    }

    setLoading(true);
    setMessage("");
    const data = new FormData();
    data.append("image", file);
    data.append("favorite_style", form.favorite_style);
    data.append("profession", form.profession);
    data.append("occasion", form.occasion);
    data.append("wellness_focus", form.wellness_focus);

    try {
      const response = await apiRequest("/analyze-face", {
        method: "POST",
        body: data,
      });
      setResult(response);
      const updatedUser = await apiRequest("/users/profile", {
        method: "PUT",
        body: JSON.stringify({
          name: user.name,
          favorite_style: form.favorite_style,
          profession: form.profession,
          occasion_preference: form.occasion,
          wellness_focus: form.wellness_focus,
        }),
      });
      onUserUpdate(updatedUser);
      onHistoryUpdate();
    } catch (err) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="view-stack">
      <section className="stat-grid">
        {stats.map((stat) => (
          <article className="stat-card" key={stat.label}>
            <span>{stat.label}</span>
            <strong>{stat.value}</strong>
          </article>
        ))}
      </section>

      <section className="advisor-grid">
        <form className="analysis-panel" onSubmit={submitAnalysis}>
          <div className="section-heading">
            <div>
              <p className="eyebrow">Face analysis</p>
              <h2>Upload and generate recommendations</h2>
            </div>
            <Upload size={22} />
          </div>

          <label className="upload-zone">
            {preview ? (
              <img src={preview} alt="Selected face preview" />
            ) : (
              <span>
                <ImagePlus size={28} />
                Select photo
              </span>
            )}
            <input type="file" accept="image/*" onChange={chooseFile} />
          </label>

          <div className="form-grid">
            <label>
              Style
              <select
                value={form.favorite_style}
                onChange={(event) => setForm({ ...form, favorite_style: event.target.value })}
              >
                <option>Smart casual</option>
                <option>Formal</option>
                <option>Streetwear</option>
                <option>Athletic</option>
                <option>Minimal classic</option>
              </select>
            </label>
            <label>
              Profession
              <input
                value={form.profession}
                onChange={(event) => setForm({ ...form, profession: event.target.value })}
                placeholder="Student, designer, engineer"
              />
            </label>
            <label>
              Occasion
              <select value={form.occasion} onChange={(event) => setForm({ ...form, occasion: event.target.value })}>
                <option>Everyday</option>
                <option>College</option>
                <option>Office</option>
                <option>Interview</option>
                <option>Event</option>
              </select>
            </label>
            <label>
              Wellness
              <select
                value={form.wellness_focus}
                onChange={(event) => setForm({ ...form, wellness_focus: event.target.value })}
              >
                <option>Energy</option>
                <option>Confidence</option>
                <option>Fitness</option>
                <option>Skin care</option>
                <option>Stress balance</option>
              </select>
            </label>
          </div>

          {message && <p className="error-text">{message}</p>}

          <button className="primary-action" disabled={loading} type="submit">
            {loading ? <RefreshCw className="spin" size={18} /> : <Sparkles size={18} />}
            Analyze style
          </button>
        </form>

        <ResultPanel result={result} />
      </section>
    </div>
  );
}

function ResultPanel({ result }) {
  if (!result) {
    return (
      <section className="result-empty">
        <Sparkles size={36} />
        <h2>Recommendations will appear here</h2>
        <div className="mini-flow">
          <span>Upload</span>
          <span>Analyze</span>
          <span>Recommend</span>
        </div>
      </section>
    );
  }

  const { analysis, recommendations } = result;

  return (
    <section className="result-panel">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Latest result</p>
          <h2>{analysis.face_shape} face shape</h2>
        </div>
        <Gauge size={22} />
      </div>

      <div className="score-grid">
        <div>
          <span>Symmetry</span>
          <strong>{Math.round(analysis.symmetry_score)}%</strong>
        </div>
        <div>
          <span>Jawline</span>
          <strong>{Math.round(analysis.jawline_score)}%</strong>
        </div>
        <div>
          <span>Contrast</span>
          <strong>{analysis.contrast_level}</strong>
        </div>
        <div>
          <span>Skin tone</span>
          <strong>{analysis.skin_tone}</strong>
        </div>
      </div>

      <RecommendationBlock icon={Scissors} title="Hair & beard" items={[...recommendations.hairstyles, recommendations.beard]} />
      <RecommendationBlock icon={Shirt} title="Outfit" items={recommendations.outfits} />
      <RecommendationBlock icon={Glasses} title="Glasses & accessories" items={[...recommendations.glasses, ...recommendations.accessories]} />

      <article className="palette-card">
        <div className="recommendation-title">
          <Palette size={18} />
          <h3>{recommendations.palette.name}</h3>
        </div>
        <div className="swatches">
          {recommendations.palette.colors.map((color) => (
            <span key={color} style={{ backgroundColor: color }} title={color} />
          ))}
        </div>
      </article>

      <RecommendationBlock icon={HeartPulse} title="Wellness" items={recommendations.wellness} />
    </section>
  );
}

function RecommendationBlock({ icon: Icon, title, items }) {
  return (
    <article className="recommendation-card">
      <div className="recommendation-title">
        <Icon size={18} />
        <h3>{title}</h3>
      </div>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </article>
  );
}

function HistoryView({ history, onSelect, onDelete }) {
  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Recommendation history</p>
          <h2>Saved analyses</h2>
        </div>
        <History size={22} />
      </div>

      {history.length === 0 ? (
        <p className="muted">No analyses saved yet.</p>
      ) : (
        <div className="history-list">
          {history.map((item) => (
            <article key={item.id} className="history-card">
              <div>
                <h3>{item.face_shape} face shape</h3>
                <p>
                  {item.skin_tone} tone, {item.contrast_level.toLowerCase()} contrast
                </p>
                <span>{formatDate(item.created_at)}</span>
              </div>
              <div className="history-actions">
                <button onClick={() => onSelect(item)} type="button">
                  Review
                </button>
                <button onClick={() => onDelete(item.id)} type="button" className="ghost-danger">
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

function ProfileView({ user, onUserUpdate }) {
  const [form, setForm] = useState({
    name: user.name,
    favorite_style: user.favorite_style || "Smart casual",
    profession: user.profession || "Student",
    occasion_preference: user.occasion_preference || "Everyday",
    wellness_focus: user.wellness_focus || "Energy",
  });
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);

  async function submitProfile(event) {
    event.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      const updated = await apiRequest("/users/profile", {
        method: "PUT",
        body: JSON.stringify(form),
      });
      onUserUpdate(updated);
      setMessage("Profile saved.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Profile</p>
          <h2>Preferences and account details</h2>
        </div>
        <User size={22} />
      </div>
      <form className="profile-form" onSubmit={submitProfile}>
        <label>
          Name
          <input value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} />
        </label>
        <label>
          Preferred style
          <select
            value={form.favorite_style}
            onChange={(event) => setForm({ ...form, favorite_style: event.target.value })}
          >
            <option>Smart casual</option>
            <option>Formal</option>
            <option>Streetwear</option>
            <option>Athletic</option>
            <option>Minimal classic</option>
          </select>
        </label>
        <label>
          Profession
          <input
            value={form.profession}
            onChange={(event) => setForm({ ...form, profession: event.target.value })}
          />
        </label>
        <label>
          Occasion
          <select
            value={form.occasion_preference}
            onChange={(event) => setForm({ ...form, occasion_preference: event.target.value })}
          >
            <option>Everyday</option>
            <option>College</option>
            <option>Office</option>
            <option>Interview</option>
            <option>Event</option>
          </select>
        </label>
        <label>
          Wellness focus
          <select
            value={form.wellness_focus}
            onChange={(event) => setForm({ ...form, wellness_focus: event.target.value })}
          >
            <option>Energy</option>
            <option>Confidence</option>
            <option>Fitness</option>
            <option>Skin care</option>
            <option>Stress balance</option>
          </select>
        </label>
        {message && <p className={message.includes("saved") ? "success-text" : "error-text"}>{message}</p>}
        <button className="primary-action" disabled={saving} type="submit">
          {saving ? <RefreshCw className="spin" size={18} /> : <User size={18} />}
          Save profile
        </button>
      </form>
    </section>
  );
}

function FeedbackView() {
  const [rating, setRating] = useState("5");
  const [comments, setComments] = useState("");
  const [message, setMessage] = useState("");
  const [saving, setSaving] = useState(false);

  async function submitFeedback(event) {
    event.preventDefault();
    setSaving(true);
    setMessage("");
    try {
      await apiRequest("/feedback", {
        method: "POST",
        body: JSON.stringify({ rating: Number(rating), comments }),
      });
      setComments("");
      setMessage("Feedback saved.");
    } catch (error) {
      setMessage(error.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Feedback</p>
          <h2>Recommendation feedback</h2>
        </div>
        <HeartPulse size={22} />
      </div>
      <form className="profile-form" onSubmit={submitFeedback}>
        <label>
          Rating
          <select value={rating} onChange={(event) => setRating(event.target.value)}>
            <option value="5">5 - Excellent</option>
            <option value="4">4 - Good</option>
            <option value="3">3 - Useful</option>
            <option value="2">2 - Needs work</option>
            <option value="1">1 - Not useful</option>
          </select>
        </label>
        <label className="wide-field">
          Comments
          <textarea
            value={comments}
            onChange={(event) => setComments(event.target.value)}
            placeholder="What should the advisor improve?"
          />
        </label>
        {message && <p className={message.includes("saved") ? "success-text" : "error-text"}>{message}</p>}
        <button className="primary-action" disabled={saving} type="submit">
          {saving ? <RefreshCw className="spin" size={18} /> : <HeartPulse size={18} />}
          Submit feedback
        </button>
      </form>
    </section>
  );
}

function GuideView() {
  const [pdf, setPdf] = useState("AI_Style_Wellness_Full_Master_Guide.pdf");
  const guides = [
    {
      file: "AI_Style_Wellness_Full_Master_Guide.pdf",
      label: "Full master guide",
    },
    {
      file: "Final_Combined_AI_Style_Wellness_Master_Guide.pdf",
      label: "Planning guide",
    },
  ];

  return (
    <section className="guide-view">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Master guide</p>
          <h2>Original PDF reference</h2>
        </div>
        <a className="secondary-action" href={`/${pdf}`} target="_blank" rel="noreferrer">
          Open PDF
        </a>
      </div>
      <div className="guide-tabs" role="tablist" aria-label="Guide PDFs">
        {guides.map((guide) => (
          <button
            key={guide.file}
            className={pdf === guide.file ? "active" : ""}
            onClick={() => setPdf(guide.file)}
            type="button"
          >
            {guide.label}
          </button>
        ))}
      </div>
      <iframe title="AI Style Wellness Guide" src={`/${pdf}`} />
    </section>
  );
}

function AdminView({ analytics, users }) {
  if (!analytics) {
    return (
      <section className="view-card">
        <p className="muted">Loading analytics...</p>
      </section>
    );
  }

  return (
    <section className="view-card">
      <div className="section-heading">
        <div>
          <p className="eyebrow">Admin analytics</p>
          <h2>System activity</h2>
        </div>
        <ShieldCheck size={22} />
      </div>

      <div className="stat-grid">
        <article className="stat-card">
          <span>Users</span>
          <strong>{analytics.total_users}</strong>
        </article>
        <article className="stat-card">
          <span>Analyses</span>
          <strong>{analytics.total_analyses}</strong>
        </article>
        <article className="stat-card">
          <span>Feedback</span>
          <strong>{analytics.feedback_count}</strong>
        </article>
      </div>

      <div className="admin-grid">
        <article>
          <h3>Face-shape distribution</h3>
          {analytics.shape_distribution.length === 0 ? (
            <p className="muted">No analysis data yet.</p>
          ) : (
            analytics.shape_distribution.map((shape) => (
              <div className="bar-row" key={shape.face_shape}>
                <span>{shape.face_shape}</span>
                <div>
                  <i style={{ width: `${Math.max(12, shape.count * 16)}%` }} />
                </div>
                <strong>{shape.count}</strong>
              </div>
            ))
          )}
        </article>
        <article>
          <h3>Latest activity</h3>
          {analytics.latest_activity.length === 0 ? (
            <p className="muted">No activity yet.</p>
          ) : (
            analytics.latest_activity.map((activity) => (
              <p className="activity-line" key={activity.id}>
                <span>{activity.name}</span>
                {activity.face_shape} at {formatDate(activity.created_at)}
              </p>
            ))
          )}
        </article>
        <article>
          <h3>Users</h3>
          {users.length === 0 ? (
            <p className="muted">No users found.</p>
          ) : (
            users.map((user) => (
              <p className="activity-line" key={user.id}>
                <span>{user.name}</span>
                {user.role} - {user.analysis_count} analyses - {user.email}
              </p>
            ))
          )}
        </article>
      </div>
    </section>
  );
}

export default function App() {
  const [user, setUser] = useState(null);
  const [view, setView] = useState("advisor");
  const [loadingUser, setLoadingUser] = useState(true);
  const [history, setHistory] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [adminUsers, setAdminUsers] = useState([]);
  const [selectedHistoryResult, setSelectedHistoryResult] = useState(null);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setLoadingUser(false);
      return;
    }
    apiRequest("/auth/me")
      .then(setUser)
      .catch(() => clearToken())
      .finally(() => setLoadingUser(false));
  }, []);

  useEffect(() => {
    if (user) {
      loadHistory();
    }
  }, [user]);

  useEffect(() => {
    if (user?.role === "admin" && view === "admin") {
      loadAnalytics();
    }
  }, [user, view]);

  async function loadHistory() {
    const data = await apiRequest("/history");
    setHistory(data);
  }

  async function loadAnalytics() {
    const [analyticsData, usersData] = await Promise.all([
      apiRequest("/admin/analytics"),
      apiRequest("/admin/users"),
    ]);
    setAnalytics(analyticsData);
    setAdminUsers(usersData);
  }

  async function logout() {
    await apiRequest("/auth/logout", { method: "POST" }).catch(() => null);
    clearToken();
    setUser(null);
    setView("advisor");
  }

  async function deleteHistoryItem(id) {
    await apiRequest(`/history/${id}`, { method: "DELETE" });
    loadHistory();
  }

  function selectHistoryItem(item) {
    setSelectedHistoryResult({ analysis: item, recommendations: item.recommendations });
    setView("advisor");
    requestAnimationFrame(() => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  if (loadingUser) {
    return (
      <main className="loading-screen">
        <RefreshCw className="spin" size={26} />
        <span>Loading advisor</span>
      </main>
    );
  }

  if (!user) {
    return <AuthScreen onAuth={setUser} />;
  }

  return (
    <div className="app-shell">
      <Sidebar view={view} setView={setView} user={user} />
      <div className="main-column">
        <Topbar user={user} onLogout={logout} />
        <main className="content-area">
          {view === "advisor" && (
            <AdvisorWithHistoryEvents
              user={user}
              onUserUpdate={setUser}
              history={history}
              onHistoryUpdate={loadHistory}
              selectedResult={selectedHistoryResult}
            />
          )}
          {view === "history" && (
            <HistoryView history={history} onSelect={selectHistoryItem} onDelete={deleteHistoryItem} />
          )}
          {view === "profile" && <ProfileView user={user} onUserUpdate={setUser} />}
          {view === "feedback" && <FeedbackView />}
          {view === "guide" && <GuideView />}
          {view === "admin" && <AdminView analytics={analytics} users={adminUsers} />}
        </main>
      </div>
    </div>
  );
}

function AdvisorWithHistoryEvents(props) {
  return <AdvisorView {...props} />;
}

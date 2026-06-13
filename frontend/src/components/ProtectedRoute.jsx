import React from "react";

export default function ProtectedRoute({ user, roles, children, fallback = null }) {
  if (!user) {
    return fallback;
  }

  if (roles?.length && !roles.includes(user.role)) {
    return (
      <section className="view-card">
        <p className="error-text">You do not have permission to open this page.</p>
      </section>
    );
  }

  return children;
}

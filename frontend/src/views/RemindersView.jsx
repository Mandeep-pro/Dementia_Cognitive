import React from 'react';
import { Bell } from 'lucide-react';
import { PillIcon, CheckIcon, BellIcon } from '../components/Icons';

export function RemindersView({ reminders = [], onToggleReminder }) {
  return (
    <div className="tab-view-container animate-fade-in">
      <div className="view-header">
        <div className="flex-between">
          <h1 className="view-title" style={{ display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
            <span>Reminders</span>
            <Bell size={22} color="#0D9488" />
          </h1>
          <span className="reminder-badge-counter">
            {reminders.filter(r => !r.completed).length} pending
          </span>
        </div>
        <p className="view-sub">Stay on track with gentle daily reminders.</p>
      </div>

      <div className="reminders-list">
        {reminders.map((reminder) => {
          const isDone = reminder.completed;

          return (
            <div
              key={reminder.id}
              className={`reminder-list-item ${isDone ? 'completed' : ''}`}
            >
              <div className="reminder-item-left">
                <div className={`reminder-icon-badge ${isDone ? 'done' : ''}`}>
                  {isDone ? (
                    <CheckIcon className="icon-done" />
                  ) : reminder.category === 'medicine' ? (
                    <PillIcon className="icon-pill" />
                  ) : (
                    <BellIcon className="icon-bell" fill="#A75A26" />
                  )}
                </div>

                <div className="reminder-item-details">
                  <h3 className={`reminder-item-title ${isDone ? 'line-through' : ''}`}>
                    {reminder.title}
                  </h3>
                  <span className="reminder-item-time">{reminder.scheduled_time}</span>
                  {reminder.subtitle && (
                    <p className="reminder-item-sub">{reminder.subtitle}</p>
                  )}
                </div>
              </div>

              <button
                onClick={() => onToggleReminder(reminder.id)}
                className={`reminder-action-btn ${isDone ? 'done' : ''}`}
                aria-label={isDone ? "Completed reminder" : "Mark as completed"}
              >
                {isDone ? (
                  <>
                    <CheckIcon className="w-4 h-4" />
                    <span>Done</span>
                  </>
                ) : (
                  <span>Mark Done</span>
                )}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}

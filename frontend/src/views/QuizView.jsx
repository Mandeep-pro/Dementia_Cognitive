import React, { useState, useEffect, useRef } from 'react';
import { Trophy, Award, Sprout, Loader2, Cloud, AlertTriangle, Sparkles } from 'lucide-react';
import {
  ChevronLeftIcon,
  SpeakerIcon,
  BrainIcon,
  ArrowRightIcon,
  ArrowLeftIcon,
  CheckIcon,
  LogoIcon
} from '../components/Icons';
import { DEFAULT_QUESTIONS } from '../api';

export function QuizView({
  questions = [],
  patient,
  gameTitle = 'Brain Boost Quiz',
  onBack,
  onCompleteQuiz
}) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [isFinished, setIsFinished] = useState(false);
  const [startTime] = useState(Date.now());
  const [quizStats, setQuizStats] = useState(null);
  const [syncStatus, setSyncStatus] = useState(null); // 'saving', 'saved', 'error'

  const speechRef = useRef(null);

  const currentQ = questions[currentIndex] || {
    id: 'q_default',
    question: 'Which animal is known for saying "meow"?',
    options: ['Cat', 'Dog', 'Cow', 'Bird'],
    answer: 'Cat'
  };

  const totalQuestions = questions.length || 5;
  const currentSelected = selectedAnswers[currentIndex];
  const progressPercent = Math.round(((currentIndex + 1) / totalQuestions) * 100);

  // Stop speech when component unmounts or question changes
  useEffect(() => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
    };
  }, [currentIndex]);

  // Read Aloud Function using Web Speech Synthesis
  const handleReadAloud = () => {
    if (!('speechSynthesis' in window)) {
      alert('Read aloud is not supported in this browser.');
      return;
    }

    if (isSpeaking) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      return;
    }

    const textToRead = `${currentQ.question}. Choose the correct answer. Option 1: ${currentQ.options[0]}. Option 2: ${currentQ.options[1]}. Option 3: ${currentQ.options[2]}. Option 4: ${currentQ.options[3]}.`;

    const utterance = new SpeechSynthesisUtterance(textToRead);
    utterance.rate = 0.88; // Gentle, slightly slower pace for elder clarity
    utterance.pitch = 1.0;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    speechRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  };

  const handleSelectOption = (option) => {
    setSelectedAnswers({
      ...selectedAnswers,
      [currentIndex]: option
    });
  };

  const handleNext = () => {
    if (currentIndex < totalQuestions - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      finishQuiz();
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    } else {
      onBack();
    }
  };

  const finishQuiz = () => {
    const timeTaken = Math.round((Date.now() - startTime) / 1000);
    let correctCount = 0;

    questions.forEach((q, idx) => {
      const selected = selectedAnswers[idx];
      if (!selected) return;

      // 1. Check if the question object itself has the answer
      let expected = q.answer;

      // 2. If not on question object, check fallback in DEFAULT_QUESTIONS
      if (!expected) {
        const found = DEFAULT_QUESTIONS.find(
          item => item.id === q.id || (item.question && q.question && item.question.trim().toLowerCase() === q.question.trim().toLowerCase())
        );
        expected = found?.answer;
      }

      // 3. Strictly compare selected option with expected answer
      if (expected && selected.trim().toLowerCase() === expected.trim().toLowerCase()) {
        correctCount += 1;
      }
    });

    const accuracy = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;
    const stats = {
      total: totalQuestions,
      correct: correctCount,
      accuracy,
      score: accuracy,
      timeTaken,
      nextDifficulty: accuracy >= 80 ? 'medium' : 'easy'
    };

    setQuizStats(stats);
    setIsFinished(true);

    if (onCompleteQuiz) {
      setSyncStatus('saving');
      Promise.resolve(onCompleteQuiz(stats))
        .then(() => {
          setSyncStatus('saved');
        })
        .catch((err) => {
          console.warn('[SmritiRoots] Quiz sync notification:', err);
          setSyncStatus('error');
        });
    }
  };

  // If Quiz is completed, display celebratory Results Screen
  if (isFinished && quizStats) {
    return (
      <div className="quiz-container quiz-result-view animate-fade-in">
        <header className="quiz-header">
          <button onClick={onBack} className="quiz-back-btn" aria-label="Go Back">
            <ChevronLeftIcon className="back-icon" />
          </button>
          <div className="brand-group">
            <LogoIcon className="brand-icon" />
            <div className="brand-text">
              <span className="brand-title">SmritiRoots</span>
              <span className="brand-tagline">Play · Remember · Live Better</span>
            </div>
          </div>
          <div style={{ width: 44 }}></div>
        </header>

        <div className="result-card">
          <div className="result-celebration-badge" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {quizStats.accuracy >= 80 ? (
              <Trophy size={48} color="#EAB308" />
            ) : quizStats.accuracy >= 50 ? (
              <Award size={48} color="#EC4899" />
            ) : (
              <Sprout size={48} color="#10B981" />
            )}
          </div>
          <h2 className="result-title">
            {quizStats.accuracy >= 80
              ? `Shabash, ${patient?.preferred_name || patient?.name || 'Friend'}!`
              : `Well Done, ${patient?.preferred_name || patient?.name || 'Friend'}!`}
          </h2>
          <p className="result-sub">
            {quizStats.accuracy >= 80
              ? `Finished ${gameTitle}. Outstanding focus and memory!`
              : `Finished ${gameTitle}. Great effort! Every practice keeps the mind active.`}
          </p>

          <div className="result-stats-grid">
            <div className="stat-box">
              <span className="stat-label">Score</span>
              <span className="stat-value">{quizStats.correct} / {quizStats.total}</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">Accuracy</span>
              <span className="stat-value">{quizStats.accuracy}%</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">Time</span>
              <span className="stat-value">{quizStats.timeTaken}s</span>
            </div>
            <div className="stat-box">
              <span className="stat-label">Mind Level</span>
              <span className="stat-value text-green" style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '4px' }}>
                {quizStats.accuracy >= 80 ? (
                  <>Sharp <Sprout size={14} color="#16A34A" /></>
                ) : quizStats.accuracy >= 50 ? (
                  <>Steady <Award size={14} color="#0D9488" /></>
                ) : (
                  <>Gentle <Sprout size={14} color="#84CC16" /></>
                )}
              </span>
            </div>
          </div>

          {/* Real-time Caregiver Sync Badge */}
          {syncStatus === 'saving' && (
            <div style={{ marginTop: '1.25rem', padding: '0.6rem 1rem', background: '#f3f4f6', color: '#4b5563', borderRadius: '10px', fontSize: '0.9rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
              <Loader2 size={16} className="animate-spin" />
              <span>Syncing activity with Caregiver...</span>
            </div>
          )}
          {syncStatus === 'saved' && (
            <div style={{ marginTop: '1.25rem', padding: '0.65rem 1rem', background: '#ecfdf5', color: '#065f46', border: '1px solid #a7f3d0', borderRadius: '10px', fontSize: '0.9rem', fontWeight: 600, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
              <Cloud size={16} />
              <span>Activity synced with Caregiver Dashboard!</span>
            </div>
          )}
          {syncStatus === 'error' && (
            <div style={{ marginTop: '1.25rem', padding: '0.65rem 1rem', background: '#fef2f2', color: '#991b1b', border: '1px solid #fecaca', borderRadius: '10px', fontSize: '0.85rem', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.5rem' }}>
              <AlertTriangle size={16} />
              <span>Result saved locally (Check server connection)</span>
            </div>
          )}

          <div className="result-actions">
            <button
              onClick={() => {
                setSelectedAnswers({});
                setCurrentIndex(0);
                setIsFinished(false);
              }}
              className="card-btn btn-secondary"
            >
              Play Again
            </button>
            <button onClick={onBack} className="card-btn btn-primary">
              Back to Home
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="quiz-container animate-fade-in">
      {/* 1. Top Header */}
      <header className="quiz-header">
        <button
          onClick={handlePrevious}
          className="quiz-back-btn"
          aria-label={currentIndex === 0 ? "Return to Home" : "Previous Question"}
        >
          <ChevronLeftIcon className="back-icon" />
        </button>

        <div className="brand-group">
          <LogoIcon className="brand-icon" />
          <div className="brand-text">
            <span className="brand-title">SmritiRoots</span>
            <span className="brand-tagline">Play · Remember · Live Better</span>
          </div>
        </div>

        {/* Read Aloud Button */}
        <button
          onClick={handleReadAloud}
          className={`read-aloud-btn ${isSpeaking ? 'speaking' : ''}`}
          aria-label="Read question and options aloud"
        >
          <SpeakerIcon className="read-aloud-icon" />
          <span>{isSpeaking ? 'Stop' : 'Read Aloud'}</span>
        </button>
      </header>

      {/* 2. Sub-header & Progress */}
      <div className="quiz-sub-header">
        <div className="quiz-meta-row">
          <span className="question-count-text">
            Question {currentIndex + 1} of {totalQuestions}
          </span>
          <div className="brain-boost-badge">
            <BrainIcon className="brain-badge-icon" />
            <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
              {currentQ.id?.startsWith('pq') ? (
                <>
                  <Sparkles size={13} color="#F59E0B" />
                  <span>Personalized</span>
                </>
              ) : (
                'Brain Boost'
              )}
            </span>
          </div>
        </div>

        {/* Green Progress Bar */}
        <div className="quiz-progress-track">
          <div
            className="quiz-progress-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* 3. Question Card (Plain text, NO image per user specifications) */}
      <div className="question-card">
        <h2 className="question-text">{currentQ.question}</h2>
        <p className="question-instruction">Choose the correct answer.</p>
      </div>

      {/* 4. Options List */}
      <div className="quiz-options-list">
        {currentQ.options?.map((option, optIdx) => {
          const isSelected = currentSelected === option;

          return (
            <button
              key={optIdx}
              onClick={() => handleSelectOption(option)}
              className={`quiz-option-card ${isSelected ? 'selected' : ''}`}
              aria-label={`Option ${optIdx + 1}: ${option}`}
              aria-checked={isSelected}
              role="radio"
            >
              <span className="option-label">{option}</span>

              {/* Radio Indicator */}
              <div className={`option-radio ${isSelected ? 'checked' : ''}`}>
                {isSelected && <div className="radio-inner-dot" />}
              </div>
            </button>
          );
        })}
      </div>

      {/* 5. Footer Navigation */}
      <div className="quiz-footer-nav">
        <button
          onClick={handlePrevious}
          className="quiz-nav-btn btn-prev"
          aria-label="Previous question"
        >
          <ArrowLeftIcon className="nav-arrow" />
          <span>Previous</span>
        </button>

        <button
          onClick={handleNext}
          disabled={!currentSelected}
          className={`quiz-nav-btn btn-next ${!currentSelected ? 'disabled' : ''}`}
          aria-label={currentIndex === totalQuestions - 1 ? "Finish quiz" : "Next question"}
        >
          <span>{currentIndex === totalQuestions - 1 ? 'Finish' : 'Next'}</span>
          <ArrowRightIcon className="nav-arrow" />
        </button>
      </div>
    </div>
  );
}

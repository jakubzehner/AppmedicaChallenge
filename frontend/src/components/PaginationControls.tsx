type Props = {
  onPrev: () => void;
  onNext: () => void;
  disablePrev: boolean;
  disableNext: boolean;
};

export function PaginationControls({
  onPrev,
  onNext,
  disablePrev,
  disableNext,
}: Props) {
  return (
    <div className="flex justify-center gap-4">
      <button
        onClick={onPrev}
        disabled={disablePrev}
        className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${
          disablePrev
            ? "text-gray-400 border-gray-200"
            : "text-gray-700 border-gray-300 hover:bg-gray-100"
        }`}
      >
        ← Poprzednia
      </button>

      <button
        onClick={onNext}
        disabled={disableNext}
        className={`px-4 py-2 rounded-lg border text-sm font-medium transition-colors ${
          disableNext
            ? "text-gray-400 border-gray-200"
            : "text-gray-700 border-gray-300 hover:bg-gray-100"
        }`}
      >
        Następna →
      </button>
    </div>
  );
}

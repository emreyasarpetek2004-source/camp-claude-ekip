export default function LogoCard({ className = "" }: { className?: string }) {
  return (
    <div
      className={`inline-flex items-center rounded-2xl bg-white px-5 py-3 shadow-card ${className}`}
    >
      <img
        src="/auscamp-logo.png"
        alt="AUSCAMP"
        width={168}
        height={32}
        className="h-8 w-auto sm:h-9"
      />
    </div>
  );
}

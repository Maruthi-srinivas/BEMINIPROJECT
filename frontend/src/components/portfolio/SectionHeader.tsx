type Props = {
  index: string;
  title: string;
  subtitle?: string;
};

export function SectionHeader({ index, title, subtitle }: Props) {
  return (
    <div className="section-header portfolio-section-header">
      <div className="section-index">{index}</div>
      <h2 className="section-title">{title}</h2>
      {subtitle ? <p className="section-sub">{subtitle}</p> : null}
      <div className="section-neon-line" aria-hidden="true" />
    </div>
  );
}

import { Link } from "react-router-dom";
import { Button } from "../components/button/Button.jsx";
import { Card, CardBody } from "../components/card/Card.jsx";

export function NotFoundPage() {
  return (
    <Card>
      <CardBody className="flex min-h-[360px] flex-col items-center justify-center text-center">
        <div className="text-sm font-semibold uppercase text-slate-400">404</div>
        <h1 className="mt-2 text-2xl font-bold text-ink">Page not found</h1>
        <p className="mt-2 max-w-md text-sm text-slate-500">The SentinelAI console route you requested does not exist.</p>
        <Link to="/dashboard" className="mt-5">
          <Button>Go to Dashboard</Button>
        </Link>
      </CardBody>
    </Card>
  );
}

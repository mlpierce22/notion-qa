import ChatSection from "./components/chat-section";
import Toggle from "./components/toggle";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-10 p-24 dark:bg-slate-800 background-gradient">
      <Toggle />
      <ChatSection />
    </main>
  );
}

import time
import schedule
import threading
import testScraping
from pprint import pprint

class SystemManager:
    """
    En klass som hanterar schemalagda jobb och sökfrågor.

    Attributes:
        query_set (set): En mängd av unika sökfrågor.
        jobs (dict): En dictionary av schemalagda jobb.
    """
    
    def __init__(self, root) -> None:
        """Skapar en ny instans av SystemManager."""
        self.running = True
        self.query_set = set()
        self.jobs = {}
        self.job_data = {}
        self.schedule_thread = threading.Thread(target=self.scheduler_loop)
        self.schedule_thread_start()
        self.root = root
        

    def run_all_queries_to_script(self, max_retries=3, attempt=1) -> None:
        """
        Kör alla sökfrågor i query_set och hämtar data. 
        Försöker igen vid fel, upp till max_retries gånger.
        """
        try:
            queries = list(self.query_set)  # Konvertera till lista för indexbaserad åtkomst
            i = 0  # Startindex för while-loopen
            while i < len(queries):  # Fortsätt så länge som index är mindre än längden på listan
                search = queries[i]
                pprint(search)  # Visa sökfrågan

                antal_matchningar = testScraping.scraping(search)  # Kör scraping
                antal_matchningar = int(antal_matchningar)  # Konvertera till int om möjligt

                pprint(antal_matchningar)  # Visa antalet matchningar
                i += 1  # Öka index för nästa iteration

        except Exception as e:
            if attempt < max_retries:
                pprint("Ett fel uppstod:", e, "Försöker igen...")
                self.run_all_queries_to_script(max_retries, attempt + 1)  # Återkalla för att försöka igen
            else:
                pprint("Misslyckades efter flera försök")  # Om max_retries nås
    
    def add_query(self, query: str) -> bool:
        """
        Lägger till en ny sökfråga i query_set.

        Args:
            query (str): En sträng som representerar sökfrågan.
        """
        if query not in self.query_set:
            self.query_set.add(query)
            self.add_job(query)
            return True
        return False

    def get_all_query(self) -> list:
        """
        Returnerar en lista med alla sökfrågor i query_set.

        Returns:
            list: En lista med sökfrågor.
        """
        return list(self.query_set)

    def delete_query(self, query) -> bool:
        """
        Tar bort en sökfråga från query_set och dess associerade jobb.

        Args:
            query (str): En sträng som representerar sökfrågan.
        """
        try:
            if query in self.query_set:
                self.query_set.remove(query)
                self.cancel_job(query)
                return True
            return False
            
        except Exception as e:
            pprint("Ett fel uppstod:", e)
    
    def run_scraping_job(self, job_name) -> None:
        """
        Kör filen testScraping
        Args:
            job_name (str): En sträng som representerar namnet på jobbet/sökfrågan.
        """
        new_value = testScraping.scraping(job_name)
        if job_name in self.job_data:
            # pprint("det finns index i listan")
            if len(self.job_data[job_name]) in [1, 2] and new_value != -1:
                # pprint("Har längd 1 eller 2 och new_value är inte -1")
                
                if len(self.job_data[job_name]) == 2:
                    # pprint("längden är två, nu sätt nya värdet på index 1")
                    self.job_data[job_name][1] = new_value
                
                if len(self.job_data[job_name]) == 1:
                    # pprint("lägger till andra sökningen")
                    self.job_data[job_name].append(new_value)
                
                if self.job_data[job_name][0] != self.job_data[job_name][1]:
                    # pprint("Första värdet är inte samma som nya") 
                    if new_value < self.job_data[job_name][0]:
                        # pprint("Nya värdet är mindre än första: Ingen alert men förnya värdet på båda")
                        self.job_data[job_name][0] = new_value
                        self.job_data[job_name][1] = new_value
                    else:
                        # pprint("ALERT!! Nya värdet är större än första: Sätt nya värdet på båda")
                        self.job_data[job_name][0] = new_value
                        self.job_data[job_name][1] = new_value
                        # Alert!! Skicka att ett nytt medelande har kommit eller
                        self.root.handle_event(f'https://www.upphandlingar.nu/?sokruta={job_name}')
        else:
            # pprint("Första körningen och sätter första index i listan")
            self.job_data[job_name] = [] # skapar en lista i dicten
            self.job_data[job_name].append(new_value) # lägger in värde i listan
            self.root.handle_event(f'https://www.upphandlingar.nu/?sokruta={job_name}')

    def add_job(self, job_name) -> None:
        """
        Skapar ett schemalagt jobb för en given sökfråga.

        Args:
            job_name (str): En sträng som representerar namnet på jobbet/sökfrågan.
        """
        self.jobs[job_name] = schedule.every(2).minutes.do(self.run_scraping_job, job_name)
        # schedule.run_continuously(interval=1)

    def cancel_job(self, job_name : str) -> None:
        """
        Avbryter ett schemalagt jobb för en given sökfråga.

        Args:
            job_name (str): En sträng som representerar namnet på jobbet/sökfrågan.
        """
        job = self.jobs.get(job_name)
        if job:
            schedule.cancel_job(job)
            del self.jobs[job_name]

    def scheduler_loop(self):
        """
        Avbryter ett schemalagt jobb för en given sökfråga.

        Args:
            job_name (str): En sträng som representerar namnet på jobbet/sökfrågan.
        """
        while self.running:
            schedule.run_pending()
            time.sleep(1)

    def stop_schedule(self):
        """
        Avbryter ett schemalagt jobb för en given sökfråga.

        Args:
            job_name (str): En sträng som representerar namnet på jobbet/sökfrågan.
        """
        # self.scheduler_loop(False)
        self.running = False
        schedule.clear()
        self.schedule_thread.join()

    def schedule_thread_start(self):
        """
        Avbryter ett schemalagt jobb för en given sökfråga.

        Args:
            job_name (str): En sträng som representerar namnet på jobbet/sökfrågan.
        """
        # Skapa och starta en tråd för att köra schemat
        self.schedule_thread.start()

# if __name__ == '__main__':
 
#     # Skapa instans av SystemManager
#     test = SystemManager()
 
#     # Skapa förfrågan
#     test.add_query("Apa")
#     test.add_query("Apda")
    
#     # # Visa trådinformation
#     # pprint(test.schedule_thread)
    
#     # Visa schemalagda jobb
#     pprint(test.jobs)
    
#     # Kör script
#     # test.run_all_queries_to_script()
 
#     # Printa alla frågor
#     # pprint(test.get_all_query())
 
#     # Radera
#     test.delete_query("Apa")
 
#     # Stoppar schedules
#     test.stop_schedule()
    
#     # Visa schemalagda jobb
#     pprint(test.jobs)
    
#     # Printa alla frågor
#     # pprint(test.get_all_query())
    
#     # # Visa trådinformation
#     # pprint(test.schedule_thread)
    
#     # 10 sekunder sleep
#     time.sleep(20)
    

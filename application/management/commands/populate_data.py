from django.core.management.base import BaseCommand
from faker import Faker
import random
import requests
from application.models import Company, Medicine, CustomerRequest, CompanyBank

class Command(BaseCommand):
    help = 'Populate the database with company, medicine, customer request, and company bank data using the OpenFDA API.'

    def handle(self, *args, **options):
        fake = Faker()

        self.stdout.write("Deleting old data...")
        Company.objects.all().delete()
        Medicine.objects.all().delete()
        CustomerRequest.objects.all().delete()
        CompanyBank.objects.all().delete()

        self.stdout.write("Fetching medicine data from OpenFDA API...")
        try:
            response = requests.get("https://api.fda.gov/drug/label.json?search=active_ingredient:acetaminophen&limit=20")
            response.raise_for_status()
        except requests.RequestException as e:
            self.stdout.write(self.style.ERROR(f"Error fetching data from OpenFDA API: {e}"))
            return

        medicines_data = response.json().get('results', [])
        if not medicines_data:
            self.stdout.write(self.style.ERROR("No medicine data found in the API response."))
            return

        # Populate companies from OpenFDA data using manufacturer_name or labeler_name
        self.stdout.write("Creating companies from OpenFDA data...")
        companies_data = {}
        for med_data in medicines_data:
            openfda = med_data.get('openfda', {})
            manufacturer_list = openfda.get('manufacturer_name') or openfda.get('labeler_name')
            if manufacturer_list:
                for name in manufacturer_list:
                    if name not in companies_data:
                        company = Company.objects.create(
                            name=name,
                            license_number=fake.bothify(text="LIC-####-????"),
                            address=fake.address(),
                            contact_number=str(fake.random_number(digits=10, fix_len=True)),
                            email=fake.email(),
                            description="Company data populated from OpenFDA API."
                        )
                        companies_data[name] = company
                        self.stdout.write(self.style.SUCCESS(f"Created Company: {name}"))

        # Fallback: if no companies were created via API, create fake ones
        if not companies_data:
            self.stdout.write("No companies from API, creating fake companies...")
            for _ in range(10):
                company = Company.objects.create(
                    name=fake.company(),
                    license_number=fake.bothify(text="LIC-####-????"),
                    address=fake.address(),
                    contact_number=str(fake.random_number(digits=10, fix_len=True)),
                    email=fake.email(),
                    description=fake.text(max_nb_chars=200)
                )
                companies_data[company.name] = company
                self.stdout.write(self.style.SUCCESS(f"Created Fake Company: {company.name}"))

        # Create fake bank accounts for each company
        self.stdout.write("Creating bank accounts for companies...")
        for company in companies_data.values():
            num_accounts = random.randint(1, 3)  # Each company gets 1 to 3 bank accounts
            for _ in range(num_accounts):
                CompanyBank.objects.create(
                    bank_account_number=fake.bban(),
                    ifsc_code=fake.bothify(text="IFSC-####-????"),
                    company=company
                )
                self.stdout.write(self.style.SUCCESS(f"Created Bank Account for {company.name}"))

        # Populate medicines using OpenFDA data
        self.stdout.write("Populating medicines from OpenFDA data...")
        for med_data in medicines_data:
            openfda = med_data.get('openfda', {})
            manufacturer_list = openfda.get('manufacturer_name') or openfda.get('labeler_name')
            if manufacturer_list:
                company = companies_data.get(manufacturer_list[0])
            else:
                # If manufacturer data is missing, assign a default company
                default_name = "Unknown Manufacturer"
                if default_name not in companies_data:
                    default_company = Company.objects.create(
                        name=default_name,
                        license_number=fake.bothify(text="LIC-####-????"),
                        address=fake.address(),
                        contact_number=str(fake.random_number(digits=10, fix_len=True)),
                        email=fake.email(),
                        description="Default company when manufacturer data is missing."
                    )
                    companies_data[default_name] = default_company
                    self.stdout.write(self.style.SUCCESS(f"Created default Company: {default_name}"))
                company = companies_data.get(default_name)

            medicine_name = openfda.get('brand_name', ['Unknown'])[0]
            try:
                Medicine.objects.create(
                    name=medicine_name,
                    medical_type="Drug",
                    buy_price=round(random.uniform(5.0, 50.0), 2),
                    sell_price=round(random.uniform(60.0, 100.0), 2),
                    c_gst=round(random.uniform(1.0, 18.0), 2),
                    s_gst=round(random.uniform(1.0, 18.0), 2),
                    batch_number=fake.bothify(text="BATCH-####"),
                    expire_date=fake.date_between(start_date="today", end_date="+2y"),
                    manufacture_date=fake.date_between(start_date="-2y", end_date="today"),
                    company=company,
                    description=med_data.get('description', ['No description available'])[0],
                    in_stock_strip=random.randint(10, 50),
                    qty_per_strip=random.randint(1, 10)
                )
                self.stdout.write(self.style.SUCCESS(f"Added Medicine: {medicine_name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Failed to add medicine record: {e}"))

        # Populate fake customer requests for testing
        self.stdout.write("Creating fake customer requests...")
        for _ in range(15):
            CustomerRequest.objects.create(
                customer_name=fake.name(),
                phone=str(fake.random_number(digits=10, fix_len=True)),
                medicine_details=fake.text(max_nb_chars=200),
                status=random.choice([True, False])
            )
        self.stdout.write(self.style.SUCCESS("Created fake customer requests."))

        self.stdout.write(self.style.SUCCESS("Database population complete using OpenFDA API!"))

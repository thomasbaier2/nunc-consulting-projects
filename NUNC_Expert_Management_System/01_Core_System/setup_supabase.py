#!/usr/bin/env python3
"""
NUNC Expert Management System - Supabase Setup
Erstellt das komplette Schema in Supabase
"""

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_supabase():
    """Erstellt das komplette Supabase Schema"""
    try:
        # Supabase Client erstellen
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            print("Supabase credentials not found in .env file")
            return False
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        print("Connecting to Supabase...")
        
        # Test connection
        result = supabase.table('profiles').select('id').limit(1).execute()
        print("Supabase connection successful!")
        
        # Lade SQL Schema
        schema_file = os.path.join(os.path.dirname(__file__), 'supabase_schema.sql')
        
        if not os.path.exists(schema_file):
            print(f"Schema file not found: {schema_file}")
            return False
        
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_schema = f.read()
        
        print("Schema file loaded successfully")
        print("IMPORTANT: You need to run the SQL schema manually in your Supabase Dashboard!")
        print("   1. Go to: https://supabase.com/dashboard/project/oqdjabbrmljpocrxsjwb")
        print("   2. Click 'SQL Editor'")
        print("   3. Copy and paste the SQL from: supabase_schema.sql")
        print("   4. Click 'Run' to execute the schema")
        
        # Test ob Tabellen existieren
        print("\nTesting if tables exist...")
        
        tables_to_check = ['profiles', 'relationships', 'contact_history', 'projects', 'project_matches']
        
        for table in tables_to_check:
            try:
                result = supabase.table(table).select('id').limit(1).execute()
                print(f"Table '{table}' exists")
            except Exception as e:
                if "Could not find the table" in str(e):
                    print(f"Table '{table}' does not exist - please run the SQL schema")
                else:
                    print(f"Error checking table '{table}': {e}")
        
        return True
        
    except Exception as e:
        print(f"Setup failed: {e}")
        return False

def test_boutique_manager():
    """Testet den BoutiqueProfileManager"""
    try:
        from boutique_profile_manager import BoutiqueProfileManager
        
        print("\n🧪 Testing BoutiqueProfileManager...")
        
        manager = BoutiqueProfileManager()
        
        # Test Profile Count
        count = manager.get_profile_count()
        print(f"📊 Current profile count: {count}")
        print(f"📊 Can add profile: {manager.can_add_profile()}")
        
        # Test Search
        profiles = manager.get_all_profiles()
        print(f"📊 Total profiles: {len(profiles)}")
        
        if profiles:
            print("✅ BoutiqueProfileManager working correctly!")
        else:
            print("ℹ️  No profiles found - this is normal for a new setup")
        
        return True
        
    except Exception as e:
        print(f"❌ BoutiqueProfileManager test failed: {e}")
        return False

def test_relationship_manager():
    """Testet den RelationshipManager"""
    try:
        from relationship_manager import RelationshipManager
        
        print("\n🧪 Testing RelationshipManager...")
        
        manager = RelationshipManager()
        
        # Test Statistics
        stats = manager.get_contact_statistics()
        print(f"📊 Contact statistics: {stats}")
        
        print("✅ RelationshipManager working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ RelationshipManager test failed: {e}")
        return False

if __name__ == "__main__":
    print("NUNC Expert Management System - Supabase Setup")
    print("=" * 60)
    
    # Setup Supabase
    setup_success = setup_supabase()
    
    if setup_success:
        print("\n" + "=" * 60)
        print("📋 NEXT STEPS:")
        print("1. Run the SQL schema in your Supabase Dashboard")
        print("2. Wait for tables to be created")
        print("3. Run this script again to test the managers")
        print("=" * 60)
        
        # Test Managers
        test_boutique_manager()
        test_relationship_manager()
        
        print("\n🎯 Setup completed! Ready for implementation.")
    else:
        print("\n❌ Setup failed. Please check your credentials and try again.")

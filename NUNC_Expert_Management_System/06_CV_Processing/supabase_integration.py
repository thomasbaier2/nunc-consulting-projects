#!/usr/bin/env python3
"""
NUNC Expert Management System - Supabase Integration
Supabase VDB Struktur und semantische Suche
"""

import os
import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import uuid

try:
    from supabase import create_client, Client
    import openai
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Installing required packages...")
    os.system("pip3 install supabase openai sentence-transformers")
    from supabase import create_client, Client
    import openai
    from sentence_transformers import SentenceTransformer

class SupabaseIntegration:
    def __init__(self, supabase_url: str = None, supabase_key: str = None, openai_api_key: str = None):
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_KEY')
        self.openai_api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        
        # Supabase Client
        if self.supabase_url and self.supabase_key:
            self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
        else:
            self.supabase = None
            print("WARNING: Supabase nicht konfiguriert - verwende lokale Datenbank")
        
        # OpenAI Client
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
            self.openai_client = openai
        else:
            self.openai_client = None
            print("WARNING: OpenAI nicht konfiguriert - verwende lokale Embeddings")
        
        # Lokale Embeddings-Model
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        except:
            self.embedding_model = None
            print("WARNING: Embedding-Model nicht verfügbar")
    
    def generate_embedding(self, text: str) -> List[float]:
        """Generiert Embedding für Text"""
        try:
            if self.openai_client:
                # OpenAI Embeddings
                response = self.openai_client.Embedding.create(
                    input=text,
                    model="text-embedding-ada-002"
                )
                return response['data'][0]['embedding']
            elif self.embedding_model:
                # Lokale Embeddings
                return self.embedding_model.encode(text).tolist()
            else:
                # Fallback: Hash-basierte "Embeddings"
                hash_obj = hashlib.sha256(text.encode())
                return [float(int(hash_obj.hexdigest()[i:i+2], 16)) / 255.0 for i in range(0, 32, 2)]
        except Exception as e:
            print(f"Fehler beim Generieren der Embeddings: {e}")
            return [0.0] * 384
    
    def insert_profile(self, profile_data: Dict[str, Any]) -> Optional[str]:
        """Fügt Profil in Supabase ein"""
        if not self.supabase:
            return self._save_locally(profile_data)
        
        try:
            supabase_data = self.prepare_profile_for_supabase(profile_data)
            
            result = self.supabase.table('profiles').insert(supabase_data).execute()
            
            if result.data:
                profile_id = result.data[0]['id']
                print(f"✅ Profil in Supabase eingefügt: {profile_id}")
                return profile_id
            else:
                print("❌ Fehler beim Einfügen in Supabase")
                return None
                
        except Exception as e:
            print(f"❌ Supabase Fehler: {e}")
            return self._save_locally(profile_data)
    
    def _save_locally(self, profile_data: Dict[str, Any]) -> str:
        """Speichert Profil lokal als Fallback"""
        local_db = "08_Output_Files/generated_profiles/supabase_local.json"
        os.makedirs("08_Output_Files/generated_profiles", exist_ok=True)
        
        # Lokale Datenbank laden
        if os.path.exists(local_db):
            with open(local_db, 'r', encoding='utf-8') as f:
                local_data = json.load(f)
        else:
            local_data = {"profiles": []}
        
        # Profil hinzufügen
        profile_id = str(uuid.uuid4())
        profile_data['id'] = profile_id
        profile_data['created_at'] = datetime.now().isoformat()
        profile_data['embedding'] = self.generate_embedding(
            f"{profile_data.get('expert_name', '')} {profile_data.get('technologien', '')}"
        )
        
        local_data["profiles"].append(profile_data)
        
        # Speichern
        with open(local_db, 'w', encoding='utf-8') as f:
            json.dump(local_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Profil lokal gespeichert: {profile_id}")
        return profile_id
    
    def prepare_profile_for_supabase(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Bereitet Profil-Daten für Supabase vor"""
        # Volltext für Embedding erstellen
        full_text = f"""
        {profile_data.get('expert_name', '')}
        {profile_data.get('hauptfokus', '')}
        {profile_data.get('zur_person', '')}
        {profile_data.get('technologien', '')}
        {profile_data.get('zertifizierungen', '')}
        {profile_data.get('methoden', '')}
        {profile_data.get('branchenkenntnisse', '')}
        """
        
        # Projekthistorie als Text
        if profile_data.get('projekthistorie'):
            for project in profile_data['projekthistorie']:
                full_text += f" {project.get('projekt_name', '')} {project.get('projektrolle', '')} {project.get('aufgaben', '')}"
        
        # Embedding generieren
        embedding = self.generate_embedding(full_text)
        
        # Supabase-kompatible Daten
        supabase_data = {
            'expert_name': profile_data.get('expert_name', ''),
            'hauptfokus': profile_data.get('hauptfokus', ''),
            'sprachen': profile_data.get('sprachen', ''),
            'zur_person': profile_data.get('zur_person', ''),
            'besondere_kenntnisse': profile_data.get('besondere_kenntnisse', ''),
            'branchenkenntnisse': profile_data.get('branchenkenntnisse', ''),
            'methoden': profile_data.get('methoden', ''),
            'technologien': profile_data.get('technologien', ''),
            'zertifizierungen': profile_data.get('zertifizierungen', ''),
            'projekthistorie': profile_data.get('projekthistorie', []),
            'embedding': embedding
        }
        
        return supabase_data
    
    def semantic_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Führt semantische Suche durch"""
        if not self.supabase:
            return self._local_semantic_search(query, limit)
        
        try:
            # Query-Embedding generieren
            query_embedding = self.generate_embedding(query)
            
            # Semantische Suche in Supabase
            result = self.supabase.rpc('match_profiles', {
                'query_embedding': query_embedding,
                'match_threshold': 0.7,
                'match_count': limit
            }).execute()
            
            return result.data if result.data else []
            
        except Exception as e:
            print(f"❌ Supabase Suche Fehler: {e}")
            return self._local_semantic_search(query, limit)
    
    def _local_semantic_search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Lokale semantische Suche als Fallback"""
        local_db = "08_Output_Files/generated_profiles/supabase_local.json"
        
        if not os.path.exists(local_db):
            return []
        
        try:
            with open(local_db, 'r', encoding='utf-8') as f:
                local_data = json.load(f)
            
            profiles = local_data.get("profiles", [])
            if not profiles:
                return []
            
            # Query-Embedding
            query_embedding = self.generate_embedding(query)
            
            # Ähnlichkeit berechnen
            results = []
            for profile in profiles:
                if 'embedding' in profile:
                    similarity = self._cosine_similarity(query_embedding, profile['embedding'])
                    if similarity > 0.3:  # Mindest-Ähnlichkeit
                        results.append({
                            **profile,
                            'similarity_score': similarity
                        })
            
            # Nach Ähnlichkeit sortieren
            results.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return results[:limit]
            
        except Exception as e:
            print(f"❌ Lokale Suche Fehler: {e}")
            return []
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Berechnet Cosinus-Ähnlichkeit zwischen zwei Vektoren"""
        try:
            import numpy as np
            
            vec1 = np.array(vec1)
            vec2 = np.array(vec2)
            
            dot_product = np.dot(vec1, vec2)
            norm1 = np.linalg.norm(vec1)
            norm2 = np.linalg.norm(vec2)
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
            
        except ImportError:
            # Fallback ohne numpy
            dot_product = sum(a * b for a, b in zip(vec1, vec2))
            norm1 = sum(a * a for a in vec1) ** 0.5
            norm2 = sum(b * b for b in vec2) ** 0.5
            
            if norm1 == 0 or norm2 == 0:
                return 0.0
            
            return dot_product / (norm1 * norm2)
    
    def get_all_profiles(self) -> List[Dict[str, Any]]:
        """Holt alle Profile aus der Datenbank"""
        if not self.supabase:
            return self._get_local_profiles()
        
        try:
            result = self.supabase.table('profiles').select('*').execute()
            return result.data if result.data else []
            
        except Exception as e:
            print(f"❌ Supabase Abfrage Fehler: {e}")
            return self._get_local_profiles()
    
    def _get_local_profiles(self) -> List[Dict[str, Any]]:
        """Holt Profile aus lokaler Datenbank"""
        local_db = "08_Output_Files/generated_profiles/supabase_local.json"
        
        if not os.path.exists(local_db):
            return []
        
        try:
            with open(local_db, 'r', encoding='utf-8') as f:
                local_data = json.load(f)
            
            return local_data.get("profiles", [])
            
        except Exception as e:
            print(f"❌ Lokale Datenbank Fehler: {e}")
            return []

def main():
    """Test der Supabase Integration"""
    print("🚀 Supabase Integration Test")
    
    # Integration initialisieren
    integration = SupabaseIntegration()
    
    # Test-Profil
    test_profile = {
        'expert_name': 'Lukas Pfanner',
        'hauptfokus': 'Salesforce Consultant',
        'sprachen': 'Deutsch/Englisch',
        'zur_person': 'Erfahrener Salesforce Consultant mit umfassender Expertise.',
        'technologien': 'Salesforce, CRM, Projektmanagement',
        'zertifizierungen': 'Salesforce Certified Administrator',
        'projekthistorie': [
            {
                'projekt_name': 'Test Projekt',
                'zeitraum': '2023-2024',
                'projektrolle': 'Consultant',
                'aufgaben': 'Beratung und Implementierung'
            }
        ]
    }
    
    # Profil einfügen
    profile_id = integration.insert_profile(test_profile)
    print(f"Profil ID: {profile_id}")
    
    # Semantische Suche testen
    search_results = integration.semantic_search("Salesforce Consultant", limit=3)
    print(f"Suche Ergebnisse: {len(search_results)}")
    
    for result in search_results:
        print(f"- {result.get('expert_name', 'Unbekannt')} (Score: {result.get('similarity_score', 0):.3f})")

if __name__ == "__main__":
    main()

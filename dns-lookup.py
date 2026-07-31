#!/usr/bin/env python3
"""
DNS Lookup Tool - Approche intermédiaire avec dnspython
"""

import dns.resolver
import dns.exception
import sys
from datetime import datetime

# Types d'enregistrements supportés
SUPPORTED_TYPES = ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA", "PTR"]


def lookup(domain, record_type="A", nameserver=None):
    """
    Effectue une requête DNS pour un type d'enregistrement donné.
    
    Args:
        domain (str): Nom de domaine ou IP (pour PTR)
        record_type (str): Type d'enregistrement (A, MX, NS, etc.)
        nameserver (str, optional): Serveur DNS personnalisé (IP)
    
    Returns:
        dict: Résultats formatés
    """
    
    # Configurer un serveur DNS personnalisé si fourni
    if nameserver:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [nameserver]
    else:
        resolver = dns.resolver.get_default_resolver()
    
    results = {
        "domain": domain,
        "record_type": record_type,
        "timestamp": datetime.now().isoformat(),
        "answers": [],
        "error": None
    }
    
    try:
        # Cas spécial pour PTR (résolution inversée)
        if record_type == "PTR":
            # Convertir IP en format arpa
            try:
                reversed_domain = dns.reversename.from_address(domain)
                answers = resolver.resolve(reversed_domain, "PTR")
            except dns.exception.SyntaxError:
                results["error"] = "Format d'IP invalide pour PTR"
                return results
        else:
            answers = resolver.resolve(domain, record_type)
        
        
        for answer in answers:
            results["answers"].append(str(answer))
            
    except dns.resolver.NoAnswer:
        results["error"] = f"Aucun enregistrement {record_type} trouvé"
    except dns.resolver.NXDOMAIN:
        results["error"] = "Domaine inexistant"
    except dns.resolver.NoNameservers:
        results["error"] = "Aucun serveur DNS disponible"
    except dns.exception.Timeout:
        results["error"] = "Requête timeout (serveur lent ou inaccessible)"
    except Exception as e:
        results["error"] = f"Erreur inattendue : {str(e)}"
    
    return results


def print_results(results):
    """Affiche les résultats de manière lisible."""
    
    print("\n" + "=" * 60)
    print(f"🔍 DNS Lookup - {results['record_type']}")
    print("=" * 60)
    print(f"📌 Domaine : {results['domain']}")
    print(f"🕐 Timestamp : {results['timestamp']}")
    print("-" * 60)
    
    if results["error"]:
        print(f"❌ Erreur : {results['error']}")
    else:
        print(f"✅ {len(results['answers'])} enregistrement(s) trouvé(s) :")
        for i, ans in enumerate(results["answers"], 1):
            print(f"   {i}. {ans}")
    
    print("=" * 60 + "\n")


def interactive_mode():
    """Mode interactif pour explorer plusieurs types."""
    
    print("\n" + "=" * 60)
    print("🖥️  DNS Lookup - Mode Interactif")
    print("=" * 60)
    
    domain = input("Domaine (ex: google.com) : ").strip()
    if not domain:
        print("Domaine requis !")
        return
    
    print(f"\nTypes supportés : {', '.join(SUPPORTED_TYPES)}")
    
    while True:
        rtype = input(f"\nType [A] ou 'quit' : ").strip().upper() or "A"
        
        if rtype.lower() == "quit":
            break
            
        if rtype not in SUPPORTED_TYPES:
            print(f"❌ Type non supporté. Choisis parmi : {', '.join(SUPPORTED_TYPES)}")
            continue
        
        results = lookup(domain, rtype)
        print_results(results)


def main():
    """Point d'entrée principal avec support CLI basique."""
    
    # Mode interactif si pas d'arguments
    if len(sys.argv) == 1:
        interactive_mode()
        return
    
    # Mode CLI simple
    # Usage: python dns_lookup.py google.com A
    #        python dns_lookup.py google.com MX
    #        python dns_lookup.py 8.8.8.8 PTR
    
    domain = sys.argv[1]
    record_type = sys.argv[2].upper() if len(sys.argv) > 2 else "A"
    
    if record_type not in SUPPORTED_TYPES:
        print(f"❌ Type {record_type} non supporté")
        print(f"Types valides : {', '.join(SUPPORTED_TYPES)}")
        sys.exit(1)
    
    results = lookup(domain, record_type)
    print_results(results)


if __name__ == "__main__":
    main()

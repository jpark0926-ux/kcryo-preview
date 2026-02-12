#!/bin/bash
# Personal Ontology - Quick Install Script

echo "🦇 Personal Ontology Setup"
echo "=========================="
echo ""

# Check if workspace directory exists
WORKSPACE="${HOME}/.openclaw/workspace"
if [ ! -d "$WORKSPACE" ]; then
    echo "❌ Workspace not found: $WORKSPACE"
    echo "Please set up OpenClaw workspace first."
    exit 1
fi

# Copy template ontology
if [ -f "$WORKSPACE/ontology.yml" ]; then
    echo "⚠️  ontology.yml already exists. Skipping copy."
else
    cp ontology-template.yml "$WORKSPACE/ontology.yml"
    echo "✅ Created $WORKSPACE/ontology.yml"
fi

# Copy scripts to workspace scripts folder
SCRIPTS_DIR="$WORKSPACE/scripts"
mkdir -p "$SCRIPTS_DIR"

for script in ontology-status.sh ontology-query.py ontology-sync.py daily-summary.sh; do
    cp "$script" "$SCRIPTS_DIR/"
    chmod +x "$SCRIPTS_DIR/$script"
    echo "✅ Installed $script"
done

# Create simulations folder
mkdir -p "$WORKSPACE/simulations"
if [ -f "simulation-example.md" ]; then
    cp simulation-example.md "$WORKSPACE/simulations/"
    echo "✅ Added simulation example"
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit $WORKSPACE/ontology.yml with your data"
echo "2. Test: cd $WORKSPACE && ./scripts/ontology-status.sh"
echo "3. Set up automation (see SKILL.md for cron examples)"
echo ""
echo "📖 Documentation: skills/personal-ontology/SKILL.md"
echo ""
